<script>
  import { onMount } from "svelte";
  import { marked } from "marked";

  import Button from "$lib/components/Button.svelte";
  import Document from "$lib/components/Document.svelte";
  import Header from "$lib/components/Header.svelte";
  import Markdown from "$lib/components/Markdown.svelte";

  let { data } = $props();

  let documentId = data.documentId;
  let documentMetadata = $state(data.documentMetadata);
  let nextTags = $state("");
  let pdfUrl = $state(null);

  const meta = $state({
    authors: data.documentMetadata.authors,
    dek: data.documentMetadata.dek,
    hed: data.documentMetadata.hed,
    year: data.documentMetadata.year,
  });

  onMount(() => {
    if (data.contentType === "application/pdf") {
      const pdfBlob = new Blob([data.data], { type: data.contentType });
      pdfUrl = URL.createObjectURL(pdfBlob);

      return () => {
        URL.revokeObjectURL(pdfUrl);
      };
    }
  });

  async function tagHandler() {
    const res = await fetch(`/api/documents/${documentId}/tags/`, {
      method: "POST",
      body: JSON.stringify({ tags: nextTags }),
    });
    documentMetadata = await res.json();
    nextTags = "";
  }

  async function putHandler() {
    const res = await fetch(`/api/documents/${documentId}`, {
      method: "PUT",
      body: JSON.stringify(meta),
    });
    documentMetadata = await res.json();
  }
</script>

<div class="Page">
  <Header />
  <div class="space left">
    <h1 class="module-title">See your document.</h1>
    <Document collapsed={false} id={documentId} meta={documentMetadata} />
    {#if documentMetadata.format === "pdf"}
      <embed src={pdfUrl} type="application/pdf" width="100%" height="700px" />
    {:else}
      <Markdown text={data.data} />
    {/if}
  </div>
  <div class="space right">
    <h1 class="module-title">Update your document.</h1>
    <div class="faux-form put-document-form">
      <div class="field">
        <h2 class="module-subhed">Update hed.</h2>
        <input bind:value={meta.hed} type="text" />
      </div>
      <div class="field">
        <h2 class="module-subhed">Update dek.</h2>
        <input bind:value={meta.dek} type="text" />
      </div>
      <div class="field">
        <h2 class="module-subhed">Update authors (comma delimited).</h2>
        <input bind:value={meta.authors} type="text" />
      </div>
      <div class="field">
        <h2 class="module-subhed">Update year.</h2>
        <input bind:value={meta.year} type="text" />
      </div>
      <div class="button-wrapper">
        <Button handler={putHandler} text="Update document." />
      </div>
    </div>
    <h1 class="module-title">Annotate your document.</h1>
    <div class="faux-form add-tags-form">
      <div class="field">
        <h2 class="module-subhed">Add a tag to your document.</h2>
        <input bind:value={nextTags} type="text" />
      </div>
      <div class="button-wrapper">
        <Button handler={tagHandler} text="Add tag." />
      </div>
    </div>
  </div>
</div>

<style>
  .space.left {
    border: 1px solid var(--color-dark);
    box-sizing: border-box;
    float: left;
    height: calc(100vh - (var(--unit) * 4));
    margin-left: var(--unit);
    overflow: scroll;
    padding: var(--unit);
    top: calc(var(--unit) * 3);
    position: relative;
    width: calc(50vw - (var(--unit) * 1.5));
  }
  .space.right {
    border: 1px solid var(--color-dark);
    box-sizing: border-box;
    float: left;
    height: calc(100vh - (var(--unit) * 4));
    margin-left: var(--unit);
    overflow: scroll;
    padding: var(--unit);
    top: calc(var(--unit) * 3);
    position: relative;
    width: calc(50vw - (var(--unit) * 1.5));
  }
  .put-document-form {
    margin-bottom: calc(var(--unit) * 2);
  }
  .field {
    margin-bottom: var(--unit);
  }
  .field h2.module-subhed {
    margin-bottom: calc(var(--unit) * 0.25);
  }
  .button-wrapper {
    margin-top: var(--unit);
  }
</style>
