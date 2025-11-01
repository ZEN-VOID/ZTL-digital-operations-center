export interface FileNode {
  id: string;
  name: string;
  type: 'file' | 'folder';
  path: string;
  size?: number;
  modifiedAt?: Date;
  children?: FileNode[];
  extension?: string;
}

export interface FileAction {
  id: string;
  label: string;
  icon: string;
  action: (file: FileNode) => void;
}

export type SortOrder = 'name' | 'date' | 'size' | 'type';
export type ViewMode = 'tree' | 'list' | 'grid';
