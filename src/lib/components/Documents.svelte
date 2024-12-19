<script>
  import { onMount } from "svelte";
  import { documentReloadCounter } from '$lib/stores.js'

  import Document from "$lib/components/Document.svelte";

  let documents = $state(null);

  onMount(async () => {
    const res = await fetch("/api/documents/");
    documents = await res.json();
  });

  $effect(async () => {
    if ($documentReloadCounter) {
      const res = await fetch("/api/documents/");
      documents = await res.json(); 
    }
  })

</script>

<div class="Documents">
  <h1 class="module-title">See your documents.</h1>
  {#if documents}
    {#each documents.ids as id, i}
      {@const meta = documents.metadatas[i]}
      <Document {id} {meta} />
    {/each}
  {/if}
</div>

<style>
  .Documents {
    box-sizing: border-box;
    max-width: 400px;
    padding: var(--unit);
    width: 100%;
  }
</style>