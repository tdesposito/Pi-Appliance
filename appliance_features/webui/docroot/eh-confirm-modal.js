class EhConfirmModal extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({ mode: "open" })
  }

  connectedCallback() {
    this._render()
    const yesButton = this.shadowRoot.querySelector(".btn-yes")
    const noButton = this.shadowRoot.querySelector(".btn-no")
    yesButton.addEventListener("click", e => {
      this.dispatchEvent(new CustomEvent("yes"))
      this.removeAttribute("visible")
      if (this.getAttribute("onConfirm")) {
        let fn
        try {
          fn = Function(this.getAttribute("onConfirm"))
        } catch (error) {
          return
        }
        if (fn) {
          fn()
        }
      }
    })
    noButton.addEventListener("click", e => {
      this.dispatchEvent(new CustomEvent("no"))
      this.removeAttribute("visible")
    })
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
          opacity: 97%;
          visibility: visible;
          transition: visibility 0s linear 0s, opacity .25s 0s;
        }
        .modal {
          background-color: #fefefe;
          border-radius: 10px;
          border: 1px solid #888;
          box-shadow: 0 4px 8px 0 rgba(0 0 0 0 / 20%),0 6px 20px 0 rgba(0 0 0 / 19%);
          left: 15%;
          min-width: 70%;
          padding: 12px;
          position: relative;
          text-align: center;
          top: 20%;
          width: 70%;
        }
        .title {
          background: #5678e5;
          border-radius: 6px;
          border: 1px solid #1499f0;
          color: white;
          font-size: 1.5rem;
          padding: 2px 16px;
        }
        .content {
          margin: 20px 2px;
          padding: 2px 16px;
        }
        .button-container {
          text-align: center;
        }
        button {
  				border-radius: 6px;
  				border: 1px solid #47a347;
  				color: #ffffff;
  				line-height: 16px;
  				margin: 6px;
  				padding: 17px 34px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 1.1rem;
          min-width: 10rem;
          opacity: .9;
          transition: opacity .25s 0s;
        }
        button.btn-yes {
          background-color: rgb(27 149 9);
          box-shadow: inset 0px 3px 12px rgba(27 149 9 / 20%);
        }
        button.btn-no {
          background-color: rgb(86 120 229);
          box-shadow: inset 0px 3px 12px rgba(86 120 229 / 20%);
        }
        button:hover {
          opacity: 1;
        }
      </style>
      <div class="${wrapperClass}">
        <div class='modal'>
          <div class='title'>${title}</div>
          <div class='content'>
            <slot></slot>
          </div>
          <div class='button-container'>
            <button class='btn-yes'>Yes</button>
            <button class='btn-no'>No - Cancel</button>
          </div>
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
window.customElements.define('eh-confirm-modal', EhConfirmModal)
