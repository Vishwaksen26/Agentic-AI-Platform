import React from 'react'
import { cn } from '../../utils/helpers'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helpText?: string
  icon?: React.ReactNode
  fullWidth?: boolean
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helpText, icon, fullWidth = true, className, ...props }, ref) => {
    return (
      <div className={fullWidth ? 'w-full' : 'inline-block'}>
        {label && (
          <label className="mb-2 block text-sm font-medium text-gray-700">{label}</label>
        )}
        <div className="relative">
          {icon && (
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              {icon}
            </div>
          )}
          <input
            ref={ref}
            className={cn(
              'w-full rounded-lg border border-gray-300 px-4 py-2 text-base',
              'focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200',
              'disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed',
              'placeholder:text-gray-400',
              error && 'border-red-500 focus:ring-red-200',
              icon && 'pl-10',
              className
            )}
            {...props}
          />
        </div>
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
        {helpText && <p className="mt-1 text-sm text-gray-500">{helpText}</p>}
      </div>
    )
  }
)

Input.displayName = 'Input'

interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  helpText?: string
  fullWidth?: boolean
}

export const TextArea = React.forwardRef<HTMLTextAreaElement, TextAreaProps>(
  ({ label, error, helpText, fullWidth = true, className, ...props }, ref) => {
    return (
      <div className={fullWidth ? 'w-full' : 'inline-block'}>
        {label && (
          <label className="mb-2 block text-sm font-medium text-gray-700">{label}</label>
        )}
        <textarea
          ref={ref}
          className={cn(
            'w-full rounded-lg border border-gray-300 px-4 py-2 text-base font-sans',
            'focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200',
            'disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed',
            'placeholder:text-gray-400',
            error && 'border-red-500 focus:ring-red-200',
            className
          )}
          {...props}
        />
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
        {helpText && <p className="mt-1 text-sm text-gray-500">{helpText}</p>}
      </div>
    )
  }
)

TextArea.displayName = 'TextArea'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  helpText?: string
  options: { value: string; label: string }[]
  fullWidth?: boolean
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, helpText, options, fullWidth = true, className, ...props }, ref) => {
    return (
      <div className={fullWidth ? 'w-full' : 'inline-block'}>
        {label && (
          <label className="mb-2 block text-sm font-medium text-gray-700">{label}</label>
        )}
        <select
          ref={ref}
          className={cn(
            'w-full rounded-lg border border-gray-300 px-4 py-2 text-base',
            'focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200',
            'disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed',
            'appearance-none bg-[url("data:image/svg+xml,%3Csvg...")]',
            error && 'border-red-500 focus:ring-red-200',
            className
          )}
          {...props}
        >
          <option value="">Select an option</option>
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
        {helpText && <p className="mt-1 text-sm text-gray-500">{helpText}</p>}
      </div>
    )
  }
)

Select.displayName = 'Select'

interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, className, ...props }, ref) => {
    return (
      <div className="flex items-center">
        <input
          ref={ref}
          type="checkbox"
          className={cn(
            'h-4 w-4 rounded border-gray-300 text-indigo-600',
            'focus:ring-indigo-500 cursor-pointer',
            className
          )}
          {...props}
        />
        {label && <label className="ml-2 text-sm text-gray-700">{label}</label>}
      </div>
    )
  }
)

Checkbox.displayName = 'Checkbox'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
  size?: 'sm' | 'md'
}

const badgeVariants = {
  default: 'bg-gray-100 text-gray-800',
  success: 'bg-green-100 text-green-800',
  warning: 'bg-yellow-100 text-yellow-800',
  danger: 'bg-red-100 text-red-800',
  info: 'bg-blue-100 text-blue-800',
}

const badgeSizes = {
  sm: 'px-2 py-1 text-xs',
  md: 'px-3 py-1 text-sm',
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ variant = 'default', size = 'md', className, children, ...props }, ref) => {
    return (
      <span
        ref={ref}
        className={cn(
          'inline-flex items-center rounded-full font-medium',
          badgeVariants[variant],
          badgeSizes[size],
          className
        )}
        {...props}
      >
        {children}
      </span>
    )
  }
)

Badge.displayName = 'Badge'
