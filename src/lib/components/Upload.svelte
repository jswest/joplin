<script>
  import Button from "$lib/components/Button.svelte";
  import { FASTAPI_PORT } from "$lib/config";
  import { documentReloadCounter } from "$lib/stores.js";

  let files;
  let working = false;
  let error = null;

  async function handleSubmit() {
    working = true;
    error = null;
    try {
      const formData = new FormData();
      formData.append("file", files[0]);

      const response = await fetch(
        `http://localhost:${FASTAPI_PORT}/documents/`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const result = await response.json();
      console.log("Upload successful:", result);
      files = undefined;
    } catch (e) {
      error = e.message;
    } finally {
      working = false;
      $documentReloadCounter += 1;
    }
  }

  function handleDragOver(e) {
    e.preventDefault();
    dragover = true;
  }

  function handleDragLeave() {
    dragover = false;
  }

  function handleDrop(e) {
    e.preventDefault();
    dragover = false;
    files = e.dataTransfer.files;
  }

  function handleClick() {
    document.getElementById("actual-file-input").click();
  }
</script>

<div class="Upload">
  <h1 class="form-title">Add a document.</h1>
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="file-upload-field"
    on:dragover={handleDragOver}
    on:dragleave={handleDragLeave}
    on:drop={handleDrop}
    on:click={handleClick}
  >
    <p>
      {#if files && files[0]}
        Selected: {files[0].name}
      {:else}
        Drop a file here to add and process it.
      {/if}
    </p>
    <input
      id="actual-file-input"
      type="file"
      bind:files
      accept=".pdf,.txt,.md"
      disabled={working}
    />
  </div>
  {#if error}
    <div class="error"><p>{error}</p></div>
  {/if}
  <div class="button-wrapper">
    <Button handler={handleSubmit} text="Add this document." />
  </div>
</div>

<style>
  .Upload {
    box-sizing: border-box;
    max-width: 400px;
    padding: var(--unit);
    width: 100%;
  }
  .error {
    background-color: var(--color-error);
  }
  .error p {
    color: var(--color-light);
    font-family: var(--font-sans);
    font-size: var(--unit);
    font-weight: 400;
    margin-top: var(--unit);
    padding: var(--unit);
  }
  .file-upload-field {
    border: 1px solid var(--color-dark);
    box-sizing: border-box;
    padding: var(--unit);
    width: 100%;
  }
  .file-upload-field p {
    font-family: var(--font-sans);
    font-size: var(--unit);
    font-weight: 100;
    line-height: 1;
  }
  input[type="file"] {
    display: none;
  }
  .button-wrapper {
    margin-top: var(--unit);
    width: 100%;
  }
</style>
