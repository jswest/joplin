<script>
  import { marked } from "marked";

  import Button from "$lib/components/Button.svelte";
  import Document from "$lib/components/Document.svelte";

  let answer = $state("");
  let documents = $state([]);
  let needles = $state(false);
  let query = $state("");

  async function handleQuestionClick() {
    answer = "";
    documents = [];
    needles = false;
    const res = await fetch("/api/query/", {
      method: "POST",
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    answer = marked.parse(data.answer.split('\n').map((graf) => graf.trim()).join('\n'));
    documents = data.documents;
  }

  async function handleSemanticClick() {
    answer = "";
    documents = [];
    needles = false;
    const res = await fetch(`/api/documents/?semantic=${query}`, {
      method: "GET",
    });
    const data = await res.json();
    needles = true;
    documents = data;
  }
</script>

<div class="Query">
  <h1 class="module-title">Talk to your documents.</h1>
  <h2 class="module-subhed">Ask a question.</h2>
  <div class="field">
    <input bind:value={query} type="text" />
  </div>
  <div class="buttons-wrapper">
    <div class="button-wrapper">
      <Button handler={handleQuestionClick} text="Ask." />
    </div>
    <div class="button-wrapper">
      <Button handler={handleSemanticClick} text="Semantic search." />
    </div>
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
  {:else if needles}
  <div class="answer">
    <h2 class="module-subhed">The semantic search responses.</h2>
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
  .buttons-wrapper .button-wrapper {
    float: left;
    width: calc(50% - (var(--unit) * 0.5));
  }
  .buttons-wrapper .button-wrapper:first-child {
    margin-right: var(--unit);
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
