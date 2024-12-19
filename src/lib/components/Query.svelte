<script>
  import { marked } from "marked";

  import Document from "$lib/components/Document.svelte";

  let answer = $state("");
  let documents = $state([]);
  let query = $state("");
  let working = $state(false);

  async function handleClick() {
    working = true;
    const res = await fetch("/api/query/", {
      method: "POST",
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    console.log(data);
    answer = marked.parse(data.answer);
    documents = data.documents;
    working = false;
  }
</script>

<div class="Query">
  <h1 class="module-title">Talk to your documents.</h1>
  <div class="field">
    <input bind:value={query} type="text" />
  </div>
  {#if !working}
    <button onclick={handleClick}>Ask.</button>
  {/if}
  {#if answer}
    <div class="answer">
      <div class="answer-guts">
        {@html answer}
      </div>
      <ul class="answer-sources">
        {#each documents as document}
          <li>
            <div class="document-wrapper">
              <Document
                id={document.document_id}
                meta={document.document_metadata}
              />
              <ul class="chunks">
                {#each document.chunk_bodies as body}
                  <li>
                    <p>{body}</p>
                  </li>
                {/each}
              </ul>
              <div style="clear:both;"></div>
            </div>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</div>

<style>
  .Query {
    border: 1px solid var(--color-dark);
    box-sizing: border-box;
    max-width: 800px;
    padding: var(--unit);
    width: 100%;
  }
  input {
    margin-bottom: var(--unit);
  }
  .answer {
    background-color: white;
    margin-top: var(--unit);
  }
  .answer :global(p) {
    font-family: var(--font-sans);
    font-size: var(--unit);
    line-height: 1.5;
    padding: var(--unit);
  }
  .answer ul {
    list-style: none;
  }
  .answer ul.answer-sources {
    margin-left: var(--unit);
  }
  .answer ul.answer-sources > li {
    border-top: 1px solid var(--color-dark);
    margin-bottom: var(--unit);
    padding-top: var(--unit);
  }
  .answer ul.chunks li {
    border: 1px solid black;
    box-sizing: border-box;
    float: left;
    height: 200px;
    margin: calc(var(--unit) * 0.5);
    overflow: scroll;
    padding: calc(var(--unit) * 0.25);
    width: 300px;
  }
  .answer ul.chunks li p {
    font-size: calc(var(--unit) * 0.75);
    line-height: 1;
  }
</style>
