<script>
  export let id;
  export let meta;
</script>

<div class="Document">
  <p class="document-id">
    <a href="/documents/{id}/">DOCUMENT-{id}</a>
  </p>
  {#if meta.hed}
    <h1>{meta.hed.slice(0, 140)}</h1>
  {/if}
  {#if meta.dek}
    <h2>{meta.dek.slice(0, 280)}</h2>
  {/if}
</div>

<style>
  .Document {
    border-left: calc(var(--unit) * 0.25) solid var(--color-dark);
    margin-bottom: var(--unit);
    padding-left: calc(var(--unit) * 0.75);
  }
  .Document .document-id {
    font-family: var(--font-sans);
    font-size: calc(var(--unit) * 0.75);
    margin-bottom: calc(var(--unit) * 0.5);
    padding: 0;
  }
  .Document h1 {
    font-family: var(--font-sans);
    font-size: var(--unit);
    font-weight: 800;
  }
  .Document h2 {
    font-family: var(--font-sans);
    font-size: var(--unit);
    font-weight: 100;
  }
</style>
