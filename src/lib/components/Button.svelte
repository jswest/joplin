<script>
  export let handler = async () => {};
  export let text = "";

  let working = false;

  async function handleClick() {
    working = true;
    try {
      await handler();
    } finally {
      working = false;
    }
  }
</script>

<div class="Button">
  {#if working}
    <div class="spinner"></div>
  {:else}
    <button onclick={handleClick}>{text}</button>
  {/if}
</div>

<style>
  .Button {
    background-color: var(--color-dark);
    box-sizing: border-box;
    height: calc(var(--unit) * 2);
    max-width: 400px;
    position: relative;
    width: 100%;
  }
  button {
    background-color: transparent;
    border: none;
    border-radius: 0;
    color: var(--color-light);
    cursor: pointer;
    font-family: var(--font-sans);
    font-size: var(--unit);
    font-weight: 800;
    line-height: 1;
    outline: none;
    padding: calc(var(--unit) / 2) var(--unit);
    text-align: left;
    width: 100%;
  }
  .spinner {
    animation: spin 1s linear infinite;
    border: 5px solid var(--color-light);
    border-radius: 50%;
    border-top: 5px solid var(--color-dark);
    box-sizing: border-box;
    height: var(--unit);
    left: calc(var(--unit));
    top: calc(var(--unit) * 0.5);
    position: absolute;
    width: var(--unit);
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
