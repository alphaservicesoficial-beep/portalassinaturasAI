const WHATSAPP_NUMBER = '5531999999999'
const WHATSAPP_MESSAGE = encodeURIComponent('Olá! Gostaria de saber mais sobre o portal de ferramentas de IA.')

function WhatsAppButton() {
  const href = "https://wa.me/5511939555495?text="

  return (
    <a
      className="whatsapp-button"
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Falar no WhatsApp"
      title="Fale conosco no WhatsApp"
    >
      <span className="whatsapp-glow" aria-hidden="true" />
      <svg
        className="whatsapp-icon"
        viewBox="0 0 24 24"
        role="presentation"
        focusable="false"
        aria-hidden="true"
      >
        <path d="M12.05 2a9.94 9.94 0 0 0-8.56 15.07l-1 3.66 3.74-.98A9.93 9.93 0 1 0 12.05 2Zm0 18a8 8 0 0 1-4.09-1.12l-.29-.17-2.22.58.59-2.16-.18-.3a7.95 7.95 0 1 1 6.19 3.17Zm4.39-5.87c-.24-.12-1.44-.71-1.67-.79s-.39-.12-.56.12-.64.79-.78.95-.29.18-.53.06a6.53 6.53 0 0 1-1.91-1.17 7 7 0 0 1-1.3-1.61c-.14-.24 0-.37.1-.49s.24-.29.36-.44a1.62 1.62 0 0 0 .24-.39.43.43 0 0 0 0-.41c-.06-.12-.53-1.27-.73-1.74s-.39-.4-.53-.4-.29 0-.44 0a.86.86 0 0 0-.63.29 2.63 2.63 0 0 0-.83 2 4.6 4.6 0 0 0 1 2.42 10.52 10.52 0 0 0 3.99 3.51 13.72 13.72 0 0 0 1.35.5 3.25 3.25 0 0 0 1.48.09 2.45 2.45 0 0 0 1.61-1.13 2 2 0 0 0 .14-1.13c-.05-.1-.2-.16-.44-.28Z" />
      </svg>
    </a>
  )
}

export default WhatsAppButton
