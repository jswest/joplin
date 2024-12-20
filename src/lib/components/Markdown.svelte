<script>
  import { marked } from "marked";

  export let text;
</script>

<div class="Markdown">
  {@html marked(text)}
</div>

<style>
  .Markdown {
    background-color: white;
    border: 1px solid var(--color-dark);
    box-sizing: border-box;
    padding: var(--unit);
    width: 100%;
  }
  .Markdown :global(p) {
    font-family: var(--font-sans);
    font-size: var(--unit);
    line-height: 1.5;
    margin-bottom: calc(var(--unit) * 1.5);
  }
  .Markdown :global(ul),
  .Markdown :global(ol) {
    font-family: var(--font-sans);
    font-size: var(--unit);
    line-height: 1.5;
    margin-left: var(--unit);
    padding-left: var(--unit);
  }
  .Markdown :global(li) {
    margin-bottom: calc(var(--unit) * 1.5);
  }
</style>
