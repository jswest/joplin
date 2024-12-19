<script>
  import Header from "$lib/components/Header.svelte";

  export let data;
  const pdfBlob = new Blob([data.pdfData], { type: data.contentType });
  const pdfUrl = URL.createObjectURL(pdfBlob);
</script>

<div class="Page">
  <Header />
  <div class="embed-wrapper">
    <embed src={pdfUrl} type="application/pdf" width="600px" height="800px" />
  </div>
</div>

<style>
  .embed-wrapper {
    margin: var(--unit);
  }
</style>