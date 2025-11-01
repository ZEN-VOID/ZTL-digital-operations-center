import { supabase, STORAGE_BUCKET, isSupabaseConfigured } from '@/lib/supabase/client';

// File validation constants
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'text/plain',
  'text/csv',
  'image/png',
  'image/jpeg',
  'image/jpg',
  'image/gif',
  'image/webp',
];

export interface UploadProgress {
  file: File;
  progress: number;
  status: 'pending' | 'uploading' | 'completed' | 'error';
  error?: string;
  url?: string;
}

export interface FileValidationResult {
  valid: boolean;
  error?: string;
}

/**
 * Validate file before upload
 */
export function validateFile(file: File): FileValidationResult {
  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      error: `文件大小超过限制 (最大 ${MAX_FILE_SIZE / 1024 / 1024}MB)`,
    };
  }

  // Check file type
  if (!ALLOWED_FILE_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: `不支持的文件类型: ${file.type}`,
    };
  }

  return { valid: true };
}

/**
 * Upload file to Supabase Storage
 */
export async function uploadFile(
  file: File,
  folder: string = 'uploads',
  onProgress?: (progress: number) => void
): Promise<{ url: string; path: string }> {
  // Check if Supabase is configured
  if (!isSupabaseConfigured() || !supabase) {
    throw new Error('Supabase未配置。请参阅 .env.local.example 配置文件上传功能。');
  }

  // Validate file
  const validation = validateFile(file);
  if (!validation.valid) {
    throw new Error(validation.error);
  }

  // Generate unique file path
  const timestamp = Date.now();
  const sanitizedFileName = file.name.replace(/[^a-zA-Z0-9.-]/g, '_');
  const filePath = `${folder}/${timestamp}_${sanitizedFileName}`;

  // Upload to Supabase Storage
  const { data, error } = await supabase.storage
    .from(STORAGE_BUCKET)
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false,
    });

  if (error) {
    throw new Error(`上传失败: ${error.message}`);
  }

  // Get public URL
  const { data: urlData } = supabase.storage
    .from(STORAGE_BUCKET)
    .getPublicUrl(filePath);

  // Save file metadata to database
  const { error: dbError } = await supabase.from('files').insert({
    name: file.name,
    path: filePath,
    size: file.size,
    type: file.type,
    folder: folder,
  });

  if (dbError) {
    console.error('Failed to save file metadata:', dbError);
    // Continue anyway - file is already uploaded
  }

  // Simulate progress for better UX (Supabase doesn't provide real-time progress)
  if (onProgress) {
    onProgress(100);
  }

  return {
    url: urlData.publicUrl,
    path: filePath,
  };
}

/**
 * Upload multiple files with progress tracking
 */
export async function uploadFiles(
  files: File[],
  folder: string = 'uploads',
  onProgress?: (fileIndex: number, progress: number) => void
): Promise<UploadProgress[]> {
  const results: UploadProgress[] = files.map((file) => ({
    file,
    progress: 0,
    status: 'pending' as const,
  }));

  // Upload files sequentially
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    results[i].status = 'uploading';

    try {
      const { url } = await uploadFile(file, folder, (progress) => {
        results[i].progress = progress;
        if (onProgress) {
          onProgress(i, progress);
        }
      });

      results[i].status = 'completed';
      results[i].progress = 100;
      results[i].url = url;
    } catch (error) {
      results[i].status = 'error';
      results[i].error = error instanceof Error ? error.message : '上传失败';
    }
  }

  return results;
}

/**
 * Delete file from Supabase Storage
 */
export async function deleteFile(filePath: string): Promise<void> {
  if (!isSupabaseConfigured() || !supabase) {
    throw new Error('Supabase未配置');
  }

  const { error } = await supabase.storage.from(STORAGE_BUCKET).remove([filePath]);

  if (error) {
    throw new Error(`删除失败: ${error.message}`);
  }

  // Delete from database
  await supabase.from('files').delete().eq('path', filePath);
}

/**
 * List files from database
 */
export async function listFiles(folder?: string) {
  if (!isSupabaseConfigured() || !supabase) {
    throw new Error('Supabase未配置');
  }

  let query = supabase.from('files').select('*').order('created_at', { ascending: false });

  if (folder) {
    query = query.eq('folder', folder);
  }

  const { data, error } = await query;

  if (error) {
    throw new Error(`获取文件列表失败: ${error.message}`);
  }

  return data;
}
