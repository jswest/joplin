<script>
  import { onMount } from "svelte";
  import Button from "$lib/components/Button.svelte";
  import Document from "$lib/components/Document.svelte";
  import Header from "$lib/components/Header.svelte";

  export let data;

  const pdfBlob = new Blob([data.pdfData], { type: data.contentType });

  let documentId = data.documentId;
  let documentMetadata = data.documentMetadata;
  let nextTags = "";
  let pdfUrl;

  onMount(() => {
    const pdfBlob = new Blob([data.pdfData], { type: data.contentType });
    pdfUrl = URL.createObjectURL(pdfBlob);

    return () => {
      URL.revokeObjectURL(pdfUrl);
    };
  });

  async function tagHandler() {
    const res = await fetch(`/api/documents/${documentId}/tags/`, {
      method: "POST",
      body: JSON.stringify({ tags: nextTags }),
    });
    documentMetadata = await res.json();
    nextTags = "";
  }
</script>

<div class="Page">
  <Header />
  <div class="space left">
    <h1 class="module-title">See your document.</h1>
    <Document id={documentId} meta={documentMetadata} />
    <embed src={pdfUrl} type="application/pdf" width="100%" height="700px" />
  </div>
  <div class="space right">
    <h1 class="module-title">Annotate your document.</h1>
    <div class="faux-form">
      <h2 class="module-subhed">Add a tag to your document.</h2>
      <input bind:value={nextTags} type="text" />
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
  .button-wrapper {
    margin-top: var(--unit);
  }
</style>
