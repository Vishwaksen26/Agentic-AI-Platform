import React from 'react'
import { cn } from '../../utils/helpers'

interface DataTableColumn<T> {
  key: keyof T
  label: string
  sortable?: boolean
  render?: (value: T[keyof T], row: T) => React.ReactNode
  width?: string
}

interface DataTableProps<T extends Record<string, unknown>> {
  columns: DataTableColumn<T>[]
  data: T[]
  keyField?: keyof T
  onRowClick?: (row: T) => void
  loading?: boolean
  empty?: React.ReactNode
  striped?: boolean
  hoverable?: boolean
}

export function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  keyField = 'id' as keyof T,
  onRowClick,
  loading = false,
  empty,
  striped = true,
  hoverable = true,
}: DataTableProps<T>) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className="w-full text-sm text-gray-600">
        <thead>
          <tr className="border-b border-gray-200 bg-gray-50">
            {columns.map((col) => (
              <th
                key={String(col.key)}
                className={cn(
                  'px-6 py-3 text-left font-semibold text-gray-900',
                  col.sortable && 'cursor-pointer hover:bg-gray-100'
                )}
                style={{ width: col.width }}
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={columns.length} className="px-6 py-8 text-center">
                <span className="text-gray-500">Loading...</span>
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="px-6 py-8 text-center">
                {empty || <span className="text-gray-500">No data</span>}
              </td>
            </tr>
          ) : (
            data.map((row, idx) => (
              <tr
                key={String(row[keyField] || idx)}
                className={cn(
                  'border-b border-gray-200',
                  striped && idx % 2 === 1 && 'bg-gray-50',
                  hoverable && 'hover:bg-gray-100',
                  onRowClick && 'cursor-pointer'
                )}
                onClick={() => onRowClick?.(row)}
              >
                {columns.map((col) => (
                  <td key={String(col.key)} className="px-6 py-4">
                    {col.render ? col.render(row[col.key], row) : String(row[col.key] || '')}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

interface StatCardProps {
  title: string
  value: string | number
  change?: number
  icon?: React.ReactNode
  trend?: 'up' | 'down' | 'neutral'
  className?: string
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  change,
  icon,
  trend,
  className,
}) => {
  return (
    <div className={cn(
      'rounded-lg border border-gray-200 bg-white p-6 shadow-sm',
      className
    )}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="mt-2 text-2xl font-bold text-gray-900">{value}</p>
          {change !== undefined && (
            <p className={cn(
              'mt-2 text-xs font-medium',
              trend === 'up' && 'text-green-600',
              trend === 'down' && 'text-red-600',
              trend === 'neutral' && 'text-gray-600'
            )}>
              {change > 0 ? '+' : ''}{change}% from last period
            </p>
          )}
        </div>
        {icon && (
          <div className="text-gray-400">{icon}</div>
        )}
      </div>
    </div>
  )
}

interface StatusIndicatorProps {
  status: 'pending' | 'active' | 'completed' | 'failed' | 'paused'
  label?: string
}

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800',
  active: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  failed: 'bg-red-100 text-red-800',
  paused: 'bg-gray-100 text-gray-800',
}

const statusDots = {
  pending: 'bg-yellow-500',
  active: 'bg-blue-500',
  completed: 'bg-green-500',
  failed: 'bg-red-500',
  paused: 'bg-gray-500',
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status, label }) => {
  return (
    <div className="flex items-center gap-2">
      <span className={cn('inline-block h-2 w-2 rounded-full', statusDots[status])} />
      <span className={cn(
        'inline-block rounded-full px-2 py-1 text-xs font-medium',
        statusColors[status]
      )}>
        {label || status.charAt(0).toUpperCase() + status.slice(1)}
      </span>
    </div>
  )
}

interface TimelineEvent {
  id: string
  title: string
  description?: string
  timestamp: string
  type: 'info' | 'success' | 'warning' | 'error'
}

interface TimelineProps {
  events: TimelineEvent[]
}

const timelineColors = {
  info: 'bg-blue-500',
  success: 'bg-green-500',
  warning: 'bg-yellow-500',
  error: 'bg-red-500',
}

export const Timeline: React.FC<TimelineProps> = ({ events }) => {
  return (
    <div className="space-y-6">
      {events.map((event, idx) => (
        <div key={event.id} className="flex gap-4">
          <div className="flex flex-col items-center">
            <div className={cn(
              'h-4 w-4 rounded-full',
              timelineColors[event.type]
            )} />
            {idx < events.length - 1 && (
              <div className="h-12 w-0.5 bg-gray-200 mt-2" />
            )}
          </div>
          <div className="flex-1">
            <h4 className="font-semibold text-gray-900">{event.title}</h4>
            {event.description && (
              <p className="mt-1 text-sm text-gray-600">{event.description}</p>
            )}
            <p className="mt-1 text-xs text-gray-500">{event.timestamp}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
