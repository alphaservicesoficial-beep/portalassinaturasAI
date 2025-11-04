function ToolCard({ title, description, image, onSelect, ...toolMeta }) {
  const handleClick = () => {
    if (onSelect) {
      onSelect({ title, description, image, ...toolMeta })
    }
  }

  return (
    <button
      type="button"
      className="tool-card"
      onClick={handleClick}
      aria-label={`Ver orientações de acesso para ${title}`}
    >
      <div className="tool-image">
        <img src={image} alt={`Mockup da ferramenta ${title}`} loading="lazy" />
      </div>
      <div className="tool-content">
        <p>{description}</p>
      </div>
    </button>
  )
}

export default ToolCard

