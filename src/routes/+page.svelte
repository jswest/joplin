<script>
  import Documents from "$lib/components/Documents.svelte";
  import Header from "$lib/components/Header.svelte";
  import Query from "$lib/components/Query.svelte";
  import Upload from "$lib/components/Upload.svelte";
</script>

<div class="Page">
  <Header />
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
  .page-guts {
    padding: calc(var(--unit) * 2);
  }
  .space.left {
    border: 1px solid var(--color-dark);
    float: left;
    height: calc(100vh - (var(--unit) * 4));
    margin-right: var(--unit);
    margin-top: var(--unit);
    overflow: scroll;
    width: 400px;
  }
  .space.center {
    border: 1px solid var(--color-dark);
    float: left;
    height: calc(100vh - (var(--unit) * 4));
    margin-top: var(--unit);
    overflow: scroll;
    width: calc(800px);
  }
  .space div {
    margin-bottom: var(--unit);
  }

</style>
