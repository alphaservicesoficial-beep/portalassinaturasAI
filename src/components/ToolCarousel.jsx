import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ToolCard from './ToolCard.jsx'

const TOUCH_BREAKPOINT_QUERY = '(max-width: 768px)'

function ToolCarousel({ tools, onSelectTool }) {
  if (!tools || tools.length === 0) {
    return null
  }

  const windowRef = useRef(null)
  const trackRef = useRef(null)
  const offsetRef = useRef(0)
  const [controls, setControls] = useState({ canGoPrev: false, canGoNext: false })
  const [isTouchMode, setIsTouchMode] = useState(false)

  const preparedTools = useMemo(() => [...tools], [tools])

  const updateTouchMode = useCallback((mediaQuery) => {
    setIsTouchMode(mediaQuery.matches)
  }, [])

  useEffect(() => {
    if (typeof window === 'undefined') return undefined

    const mq = window.matchMedia(TOUCH_BREAKPOINT_QUERY)
    updateTouchMode(mq)
    const handler = (event) => updateTouchMode(event)
    mq.addEventListener('change', handler)

    return () => {
      mq.removeEventListener('change', handler)
    }
  }, [updateTouchMode])

  const updateControls = useCallback(() => {
    if (isTouchMode) {
      setControls({ canGoPrev: false, canGoNext: false })
      return
    }

    const container = windowRef.current
    const track = trackRef.current

    if (!container || !track) return

    const minOffset = Math.min(container.clientWidth - track.scrollWidth, 0)
    const tolerance = 1

    if (offsetRef.current < minOffset) {
      offsetRef.current = minOffset
      track.style.setProperty('--track-offset', `${offsetRef.current}px`)
    }

    if (offsetRef.current > 0) {
      offsetRef.current = 0
      track.style.setProperty('--track-offset', '0px')
    }

    setControls({
      canGoPrev: offsetRef.current < -tolerance,
      canGoNext: offsetRef.current > minOffset + tolerance,
    })
  }, [isTouchMode])

  useEffect(() => {
    updateControls()

    if (typeof window === 'undefined') {
      return undefined
    }

    const handleResize = () => updateControls()
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [updateControls])

  useEffect(() => {
    offsetRef.current = 0
    if (trackRef.current) {
      trackRef.current.style.setProperty('--track-offset', '0px')
    }
    updateControls()
  }, [preparedTools, updateControls])

  const shiftBy = useCallback(
    (step) => {
      if (isTouchMode) {
        return
      }

      const container = windowRef.current
      const track = trackRef.current

      if (!container || !track || typeof window === 'undefined') {
        return
      }

      const card = track.querySelector('.manual-carousel-item')
      if (!card) return

      const { width } = card.getBoundingClientRect()
      const style = window.getComputedStyle(track)
      const gap = parseFloat(style.columnGap || style.gap || '0')
      const distance = (width + gap) * step

      const minOffset = Math.min(container.clientWidth - track.scrollWidth, 0)
      const maxOffset = 0
      const nextOffset = Math.max(Math.min(offsetRef.current - distance, maxOffset), minOffset)

      if (nextOffset === offsetRef.current) {
        return
      }

      offsetRef.current = nextOffset
      track.style.setProperty('--track-offset', `${offsetRef.current}px`)
      window.requestAnimationFrame(updateControls)
    },
    [isTouchMode, updateControls],
  )

  const windowClassName = isTouchMode
    ? 'manual-carousel-window manual-carousel-window--touch'
    : 'manual-carousel-window'

  const trackClassName = isTouchMode
    ? 'manual-carousel-track manual-carousel-track--touch'
    : 'manual-carousel-track'

  const itemClassName = isTouchMode
    ? 'manual-carousel-item manual-carousel-item--touch'
    : 'manual-carousel-item'

  return (
    <div className="tools-carousel manual-mode">
      {!isTouchMode && (
        <button
          type="button"
          className="carousel-manual-button prev"
          onClick={() => shiftBy(-1)}
          aria-label="Ver cards anteriores"
          disabled={!controls.canGoPrev}
        >
          {'<'}
        </button>
      )}

      <div className={windowClassName} ref={windowRef}>
        <div
          ref={trackRef}
          className={trackClassName}
          style={isTouchMode ? undefined : { '--track-offset': '0px' }}
        >
          {preparedTools.map((tool) => (
            <div className={itemClassName} key={tool.title}>
              <ToolCard {...tool} onSelect={onSelectTool} />
            </div>
          ))}
        </div>
      </div>

      {!isTouchMode && (
        <button
          type="button"
          className="carousel-manual-button next"
          onClick={() => shiftBy(1)}
          aria-label="Ver próximos cards"
          disabled={!controls.canGoNext}
        >
          {'>'}
        </button>
      )}
    </div>
  )
}

export default ToolCarousel
