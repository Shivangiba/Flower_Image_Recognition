'use client'
import * as React from 'react'
import {
  useFloating,
  autoUpdate,
  offset,
  flip,
  shift,
  useHover,
  useFocus,
  useDismiss,
  useRole,
  useInteractions,
  FloatingPortal,
} from '@floating-ui/react'

interface TooltipProps {
  children: React.ReactElement
  content: React.ReactNode
}

export function Tooltip({ children, content }: TooltipProps) {
  const [isOpen, setIsOpen] = React.useState(false)

  const { refs, floatingStyles, context } = useFloating({
    open: isOpen,
    onOpenChange: setIsOpen,
    placement: 'top',
    whileElementsMounted: autoUpdate,
    middleware: [
      offset(10),
      flip({
        fallbackAxisSideDirection: 'start',
      }),
      shift(),
    ],
  })

  const hover = useHover(context, { move: false })
  const focus = useFocus(context)
  const dismiss = useDismiss(context)
  const role = useRole(context, { role: 'tooltip' })

  const { getReferenceProps, getFloatingProps } = useInteractions([
    hover,
    focus,
    dismiss,
    role,
  ])

  return (
    <>
      {React.cloneElement(children, getReferenceProps({ 
        ref: refs.setReference, 
        ...(children.props as any) 
      }))}

      <FloatingPortal>
        {isOpen && (
          <div
            className="z-50 px-4 py-2 text-sm font-bold text-white glass border border-brand-primary/20 rounded-xl shadow-2xl backdrop-blur-xl animate-in fade-in zoom-in duration-200"
            ref={refs.setFloating}
            style={floatingStyles}
            {...getFloatingProps()}
          >
            {content}
          </div>
        )}
      </FloatingPortal>
    </>
  )
}
