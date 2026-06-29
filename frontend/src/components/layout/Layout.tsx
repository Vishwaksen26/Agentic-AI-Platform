import React from 'react'
import { cn } from '../../utils/helpers'
import { Menu, X } from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
  sidebar?: React.ReactNode
  header?: React.ReactNode
  footer?: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children, sidebar, header, footer }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(true)

  return (
    <div className="flex h-screen bg-gray-50">
      {sidebar && (
        <>
          {/* Mobile sidebar backdrop */}
          {sidebarOpen && (
            <div
              className="fixed inset-0 z-20 bg-black/50 md:hidden"
              onClick={() => setSidebarOpen(false)}
            />
          )}
          {/* Sidebar */}
          <div className={cn(
            'fixed inset-y-0 left-0 z-30 w-64 bg-white shadow-lg transition-transform md:relative md:translate-x-0',
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          )}>
            {sidebar}
          </div>
        </>
      )}

      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        {header && (
          <header className="border-b border-gray-200 bg-white shadow-sm">
            <div className="flex items-center justify-between px-6 py-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden text-gray-600 hover:text-gray-900"
              >
                {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
              {header}
            </div>
          </header>
        )}

        {/* Main content */}
        <main className="flex-1 overflow-auto">
          <div className="p-6">
            {children}
          </div>
        </main>

        {/* Footer */}
        {footer && (
          <footer className="border-t border-gray-200 bg-white px-6 py-4">
            {footer}
          </footer>
        )}
      </div>
    </div>
  )
}

interface SidebarProps {
  logo?: React.ReactNode
  items: SidebarItem[]
  activeItem?: string
  onItemClick?: (id: string) => void
  footer?: React.ReactNode
}

interface SidebarItem {
  id: string
  label: string
  icon?: React.ReactNode
  href?: string
  items?: SidebarItem[]
  divider?: boolean
}

export const Sidebar: React.FC<SidebarProps> = ({
  logo,
  items,
  activeItem,
  onItemClick,
  footer,
}) => {
  const [expanded, setExpanded] = React.useState<Set<string>>(new Set())

  const toggleExpanded = (id: string) => {
    const newExpanded = new Set(expanded)
    if (newExpanded.has(id)) {
      newExpanded.delete(id)
    } else {
      newExpanded.add(id)
    }
    setExpanded(newExpanded)
  }

  return (
    <div className="flex h-full flex-col">
      {logo && (
        <div className="border-b border-gray-200 px-6 py-4">
          {logo}
        </div>
      )}

      <nav className="flex-1 space-y-1 px-3 py-4">
        {items.map((item) => (
          <React.Fragment key={item.id}>
            {item.divider && <div className="my-4 border-t border-gray-200" />}
            <SidebarItemComponent
              item={item}
              isActive={activeItem === item.id}
              isExpanded={expanded.has(item.id)}
              onToggle={() => toggleExpanded(item.id)}
              onClick={() => onItemClick?.(item.id)}
              level={0}
            />
          </React.Fragment>
        ))}
      </nav>

      {footer && (
        <div className="border-t border-gray-200 px-6 py-4">
          {footer}
        </div>
      )}
    </div>
  )
}

interface SidebarItemComponentProps {
  item: SidebarItem
  isActive: boolean
  isExpanded: boolean
  onToggle: () => void
  onClick: () => void
  level: number
}

const SidebarItemComponent: React.FC<SidebarItemComponentProps> = ({
  item,
  isActive,
  isExpanded,
  onToggle,
  onClick,
  level,
}) => {
  return (
    <div>
      <button
        onClick={() => {
          onClick()
          if (item.items?.length) onToggle()
        }}
        className={cn(
          'flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
          isActive ? 'bg-indigo-100 text-indigo-900' : 'text-gray-700 hover:bg-gray-100'
        )}
        style={{ paddingLeft: `${12 + level * 12}px` }}
      >
        {item.icon && <span className="flex-shrink-0">{item.icon}</span>}
        <span className="flex-1 text-left">{item.label}</span>
        {item.items?.length && (
          <span className={cn(
            'flex-shrink-0 transition-transform',
            isExpanded && 'rotate-180'
          )}>
            ▼
          </span>
        )}
      </button>

      {item.items?.length && isExpanded && (
        <div className="space-y-1">
          {item.items.map((subItem) => (
            <SidebarItemComponent
              key={subItem.id}
              item={subItem}
              isActive={false}
              isExpanded={false}
              onToggle={() => {}}
              onClick={() => {}}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  )
}

interface BreadcrumbProps {
  items: BreadcrumbItem[]
}

interface BreadcrumbItem {
  label: string
  href?: string
  onClick?: () => void
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({ items }) => {
  return (
    <nav className="flex items-center gap-2 text-sm">
      {items.map((item, idx) => (
        <React.Fragment key={idx}>
          {idx > 0 && <span className="text-gray-400">/</span>}
          {item.href || item.onClick ? (
            <a
              href={item.href}
              onClick={(e) => {
                if (item.onClick) {
                  e.preventDefault()
                  item.onClick()
                }
              }}
              className="text-indigo-600 hover:text-indigo-700"
            >
              {item.label}
            </a>
          ) : (
            <span className="text-gray-900">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  )
}
