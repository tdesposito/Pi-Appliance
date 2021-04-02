class EhLoadingModal extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({ mode: "open" })
  }

  connectedCallback() {
    this._render()
  }

  get visible() {
    return this.hasAttribute("visible")
  }
  set visible(value) {
    if (value) {
      this.setAttribute("visible", "")
    } else {
      this.removeAttribute("visible")
    }
  }

  static get observedAttributes() {
    return ["visible"]
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (this.shadowRoot) {
      if (name === "visible" && this.shadowRoot.querySelector(".wrapper")) {
        if (newValue === null) {
          this.shadowRoot.querySelector(".wrapper").classList.remove("visible")
        } else {
          this.shadowRoot.querySelector(".wrapper").classList.add("visible")
        }
      }
    }
  }

  _render() {
    const wrapperClass = this.visible ? "wrapper visible" : "wrapper"
    const title = this.title ? this.title : "default title"
    const container = document.createElement("div")
    container.innerHTML = `
      <style>
        .wrapper {
          background-color: gray;
          height: 100%;
          left: 0;
          opacity: 0;
          position: fixed;
          top: 0;
          visibility: hidden;
          width: 100%;
          z-index: 1;
        }
        .visible {
          opacity: 95%;
          visibility: visible;
          transition: visibility 0s linear 0s, opacity .25s 0s;
        }
        .content {
          font-size: 2.5rem;
          height: 100%;
          margin: 20px 2px;
          padding: 2px 16px;
          position: relative;
          text-align: center;
          top: 30%;
          vertical-align: middle;
        }
      </style>
      <div class="${wrapperClass}">
        <div class='content'>
          <slot>
            Loading...
          </slot>
        </div>
      </div>
    `
    this.shadowRoot.appendChild(container)
  }

  show = function() {
    this.setAttribute("visible", "")
  }
  hide = function() {
    this.removeAttribute("visible")
  }
}
window.customElements.define('eh-loading-modal', EhLoadingModal)
