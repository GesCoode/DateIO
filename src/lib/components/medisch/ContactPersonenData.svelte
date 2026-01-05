<script lang="ts">
    import ContactPersoon from "$lib/components/medisch/ContactPersoon.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";

    export let handleOpslaan: () => void = () => {};

    let textareas: { id: number; value: string }[] = [{ id: 1, value: "" }];
    let errorMessage: string = "";

    function handleVermeldingToevoegen() {
        if (textareas.length >= 6) {
            errorMessage = "U kunt maximaal 6 personen toevoegen";
            return;
        }

        const newId = Math.max(...textareas.map((t) => t.id)) + 1;
        textareas = [...textareas, { id: newId, value: "" }];
        errorMessage = "";
    }

    function handleVermeldingVerwijderen(id: number) {
        textareas = textareas.filter((t) => t.id !== id);
        errorMessage = "";
    }
</script>

<div class="flex flex-col gap-4">
    {#each textareas as textarea, index (textarea.id)}
        <ContactPersoon
            nummer={index + 1}
            deletable={textareas.length > 1}
            on:delete={() => handleVermeldingVerwijderen(textarea.id)}
        />
    {/each}

    {#if errorMessage}
        <div class="text-red-600 text-sm">{errorMessage}</div>
    {/if}
</div>

<!-- Buttons -->
<div class="flex flex-row items-start gap-2 mt-4">
    <div class="flex flex-col items-start">
        <SimpleButton
            text="Opslaan"
            bgColor="#0C3966"
            textColor="#FFF"
            onClick={handleOpslaan}
        />
    </div>
    <div class="flex flex-col items-start">
        <SimpleButton
            text="Persoon toevoegen"
            bgColor="#0C3966"
            textColor="#FFF"
            onClick={handleVermeldingToevoegen}
        />
    </div>
</div>
