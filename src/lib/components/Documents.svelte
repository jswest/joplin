<script>
  import { onMount } from "svelte";

  import Document from "$lib/components/Document.svelte";

  let documents = $state(null);

  onMount(async () => {
    const res = await fetch("/api/documents/");
    documents = await res.json();
  });
</script>

<div class="Documents">
  <h1 class="module-title">Documents</h1>
  {#if documents}
    {#each documents.ids as id, i}
      {@const meta = documents.metadatas[i]}
      <Document {id} {meta} />
    {/each}
  {/if}
</div>

<style>
  .Documents {
    border: 1px solid var(--color-dark);
    box-sizing: border-box;
    max-width: 400px;
    padding: var(--unit);
    width: 100%;
  }
</style>