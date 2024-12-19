<script>
  export let name;
  export let xHandler;
</script>

<span class="Token">
  {#if xHandler}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <span class="x" onclick={xHandler}>X</span>
  {/if}
  <span class="name {xHandler ? 'has-x' : ''}">
    {name}
  </span>
</span>

<style>
  .Token {
    background-color: var(--color-dark);
    margin-right: calc(var(--unit) * 0.25);
  }
  .Token .name {
    color: var(--color-light);
    font-family: var(--font-sans);
    font-size: calc(var(--unit) * 0.6);
    font-weight: 800;
    padding: calc(var(--unit) * 0.2) calc(var(--unit) * 0.25);
  }
  .Token .name.has-x {
    padding-left: 0;
  }
  .Token .x {
    border-right: 1px dotted var(--color-light);
    color: var(--color-light);
    cursor: pointer;
    font-family: var(--font-sans);
    font-size: calc(var(--unit) * 0.6);
    font-weight: 100;
    margin-right: calc(var(--unit) * 0.25);
    padding: calc(var(--unit) * 0.25);
  }
</style>