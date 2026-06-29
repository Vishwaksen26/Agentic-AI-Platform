import React from 'react'
import { cn } from '../../utils/helpers'
import { X } from 'lucide-react'

interface DialogProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl'
  footer?: React.ReactNode
}

const sizeClasses = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-xl',
}

export const Dialog: React.FC<DialogProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  footer,
}) => {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div
        className={cn(
          'relative w-full rounded-lg bg-white shadow-xl',
          sizeClasses[size]
        )}
      >
        {title && (
          <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
            <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              <X size={24} />
            </button>
          </div>
        )}
        <div className="px-6 py-4">{children}</div>
        {footer && (
          <div className="border-t border-gray-200 px-6 py-3">{footer}</div>
        )}
      </div>
    </div>
  )
}

interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  type?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  icon?: React.ReactNode
}

const alertStyles = {
  success: 'bg-green-50 border-green-200 text-green-800',
  error: 'bg-red-50 border-red-200 text-red-800',
  warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
  info: 'bg-blue-50 border-blue-200 text-blue-800',
}

export const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ type = 'info', title, message, icon, className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'flex gap-3 rounded-lg border px-4 py-3',
          alertStyles[type],
          className
        )}
        {...props}
      >
        {icon && <div className="flex-shrink-0">{icon}</div>}
        <div className="flex-1">
          {title && <h4 className="font-medium">{title}</h4>}
          <p className="text-sm">{message}</p>
        </div>
      </div>
    )
  }
)

Alert.displayName = 'Alert'

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number
  max?: number
  showLabel?: boolean
  variant?: 'default' | 'success' | 'warning' | 'danger'
}

const progressVariants = {
  default: 'bg-indigo-600',
  success: 'bg-green-600',
  warning: 'bg-yellow-600',
  danger: 'bg-red-600',
}

export const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  (
    { value, max = 100, showLabel = false, variant = 'default', className, ...props },
    ref
  ) => {
    const percentage = Math.min((value / max) * 100, 100)

    return (
      <div ref={ref} className={cn('w-full', className)} {...props}>
        <div className="flex items-center justify-between mb-2">
          <div className="h-2 flex-1 rounded-full bg-gray-200">
            <div
              className={cn('h-full rounded-full transition-all', progressVariants[variant])}
              style={{ width: `${percentage}%` }}
            />
          </div>
          {showLabel && <span className="ml-2 text-sm font-medium text-gray-700">{Math.round(percentage)}%</span>}
        </div>
      </div>
    )
  }
)

Progress.displayName = 'Progress'

interface LoadingSpinnerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg'
}

const sizeMap = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ size = 'md', className, ...props }) => {
  return (
    <div
      className={cn(
        'animate-spin rounded-full border-2 border-gray-300 border-t-indigo-600',
        sizeMap[size],
        className
      )}
      {...props}
    />
  )
}

interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: React.ReactNode
}

export const EmptyState: React.FC<EmptyStateProps> = ({ icon, title, description, action }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      {icon && <div className="mb-4 text-gray-400">{icon}</div>}
      <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      {description && <p className="mt-2 text-sm text-gray-600">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
