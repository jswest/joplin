<script>
  import { ChevronDown, ChevronRight } from "lucide-svelte";

  import Markdown from "$lib/components/Markdown.svelte";

  export let collapsed = true;
  export let summary;
</script>

<div class="Summary">
  {#if collapsed}
    <h2 class="module-subhed">
      <button class="transparent-button" onclick={() => (collapsed = false)}>
        <ChevronRight size="12" />
      </button>
      Read the AI summary.
    </h2>
  {:else}
    <h2 class="module-subhed">
      <button class="transparent-button" onclick={() => (collapsed = true)}>
        <ChevronDown size="12" />
      </button>
      AI Summary
    </h2>
    <Markdown text={summary} />
  {/if}
</div>
