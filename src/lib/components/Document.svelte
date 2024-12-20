<script>
  import { ChevronDown, ChevronRight } from "lucide-svelte";

  import Token from "$lib/components/Token.svelte";
  import { getArrayField } from "$lib/utils.js";

  export let collapsed = true;
  export let id;
  export let meta;

  async function tagXHandler(tag) {
    const res = await fetch(`/api/documents/${id}/tags/`, {
      method: "DELETE",
      body: JSON.stringify({ tag }),
    });
    meta = await res.json();
  }
</script>

<div class="Document">
  {#if collapsed}
    <h1 >
      <button class="transparent-button" onclick={() => (collapsed = false)}>
        <ChevronRight size="12" />
      </button>
      <a href="/documents/{id}/">{meta.hed}</a>
    </h1>
  {:else}
    <h1>
      <button class="transparent-button" onclick={() => (collapsed = true)}>
        <ChevronDown size="12" />
      </button>
      <a href="/documents/{id}/">
        {#if meta.hed}
          {meta.hed.slice(0, 140).trim()}
          {#if meta.year}
            ({meta.year})
          {/if}
        {:else}
          {id}
        {/if}
      </a>
    </h1>
    {#if meta.dek}
      <h2>{meta.dek.slice(0, 280).trim()}</h2>
    {/if}
    {#if meta.authors}
      <p class="authors">
        <span class="byline">by:</span>
        {#each getArrayField(meta.authors) as author}
          <Token name={author} />
        {/each}
      </p>
    {/if}
    {#if meta.tags}
      <p class="tags">
        tags:
        {#each getArrayField(meta.tags) as tag}
          <Token
            name={tag}
            xHandler={async () => {
              await tagXHandler(tag);
            }}
          />
        {/each}
      </p>
    {/if}
    <p class="created-at">
      created at: {new Date(meta.created_at).toLocaleString("en-US")}
    </p>
    <p class="format">
      format: <Token name={meta.format} />
    </p>
  {/if}
</div>

<style>
  .Document {
    border-left: calc(var(--unit) * 0.25) solid var(--color-dark);
    margin-bottom: var(--unit);
    padding-left: calc(var(--unit) * 0.75);
  }
  .Document .authors,
  .Document .created-at,
  .Document .document-id,
  .Document .format,
  .Document .tags {
    font-family: var(--font-sans);
    font-size: calc(var(--unit) * 0.75);
    font-weight: 100;
    line-height: 1.5;
    padding: 0;
  }
  .Document h1 {
    font-family: var(--font-sans);
    font-size: calc(var(--unit) * 0.75);
    font-weight: 800;
  }
  .Document h2 {
    font-family: var(--font-sans);
    font-size: calc(var(--unit) * 0.75);
    font-weight: 400;
    margin-bottom: calc(var(--unit) * 0.25);
  }
  .transparent-button {
    background-color: transparent;
    border: none;
    border-radius: 0;
    cursor: pointer;
    outline: none;
  }
</style>
