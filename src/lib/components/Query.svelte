<script>
  import { marked } from "marked";

  import Button from "$lib/components/Button.svelte";
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
    answer = marked.parse(data.answer.split('\n').map((graf) => graf.trim()).join('\n'));
    documents = data.documents;
    working = false;
  }
</script>

<div class="Query">
  <h1 class="module-title">Talk to your documents.</h1>
  <h2 class="module-subhed">Ask a question.</h2>
  <div class="field">
    <input bind:value={query} type="text" />
  </div>
  <div class="button-wrapper">
    <Button handler={handleClick} text="Ask." />
  </div>
  {#if answer}
    <div class="answer">
      <h2 class="module-subhed">The AI answer.</h2>
      <div class="answer-guts">
        {@html answer}
      </div>
      <h2 class="module-subhed">The AI sources.</h2>
      <ul class="answer-sources">
        {#each documents as document}
          <li>
            <div class="document-wrapper">
              <Document
                id={document.document_id}
                meta={document.document_metadata}
              />
            </div>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</div>

<style>
  .Query {
    box-sizing: border-box;
    max-width: 800px;
    padding: var(--unit);
    width: 100%;
  }
  input {
    margin-bottom: var(--unit);
  }
  .button-wrapper {
    margin-bottom: var(--unit);
  }
  .answer-guts {
    background-color: white;
    margin-bottom: var(--unit);
    margin-top: var(--unit);
  }
  .answer-guts :global(p) {
    font-family: var(--font-sans);
    font-size: var(--unit);
    line-height: 1.5;
    padding: var(--unit);
  }
  .answer ul {
    list-style: none;
  }
  .answer ul.answer-sources li {
    margin-bottom: var(--unit);
  }
</style>
