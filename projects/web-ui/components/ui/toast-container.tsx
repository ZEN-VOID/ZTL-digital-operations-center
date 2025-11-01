'use client';

import * as React from 'react';
import { useToast } from '@/lib/hooks/use-toast';
import { Toast, Toaster } from './toast';

export interface ToastContainerProps {
  position?: 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right';
}

export function ToastContainer({ position = 'top-right' }: ToastContainerProps) {
  const { toasts, dismiss } = useToast();

  return (
    <Toaster position={position}>
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          id={toast.id}
          title={toast.title}
          description={toast.description}
          variant={toast.variant}
          duration={toast.duration}
          onClose={dismiss}
        />
      ))}
    </Toaster>
  );
}
