<script>
  import Documents from "$lib/components/Documents.svelte";
  import Query from "$lib/components/Query.svelte";
  import Upload from "$lib/components/Upload.svelte";
</script>

<div class="Page">
  <header>
    <h1><span class="title">Joplin.</span> It's RAG time for your laptop.</h1>
  </header>
  <div class="page-guts">
    <div class="space left">
      <div>
        <Upload />
      </div>
      <div>
        <Documents />
      </div>
    </div>
    <div class="space center">
      <div>
        <Query />
      </div>
    </div>
  </div>
</div>

<style>
  header {
    background-color: var(--color-dark);
    padding: calc(var(--unit) * 0.5) calc(var(--unit) * 2);
  }
  header h1 {
    color: var(--color-light);
    font-family: var(--font-sans);
    font-size: var(--unit);
    font-weight: 100;
  }
  header h1 .title {
    color: var(--color-light);
    font-weight: 800;
  }
  .page-guts {
    padding: calc(var(--unit) * 2);
  }
  .space.left {
    float: left;
    margin-right: var(--unit);
    width: 400px;
  }
  .space.center {
    float: left;
    width: calc(800px);
  }
  .space div {
    margin-bottom: var(--unit);
  }

</style>
