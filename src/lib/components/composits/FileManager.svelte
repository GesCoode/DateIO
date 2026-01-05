<script lang="ts">
    import OutputField from "$lib/components/form/OutputField.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";

    export let file: File | null = null;
    export let onRemove: () => void = () => {};
    export let onError: (message: string) => void = () => {};

    function handleVoegToe() {
        const input = document.createElement("input");
        input.type = "file";
        input.multiple = false;

        input.onchange = () => {
            if (!input.files || input.files.length === 0) return;

            const selectedFile = input.files[0];
            const maxSize = 5 * 1024 * 1024;

            if (selectedFile.size > maxSize) {
                onError("Bestand is te groot (max 5MB)");
                return;
            }

            file = selectedFile;
            onError(""); // clear error on success
        };

        input.click();
    }
</script>

<div class="flex flex-col w-full bg-[#0C3966] rounded p-2">
    <div class="flex justify-end mb-1">
        {#if file}
            <button
                class="text-white font-bold rounded hover:bg-white/20"
                on:click={onRemove}
                aria-label="Verwijder bestand"
            >
                ✕
            </button>
        {/if}
    </div>

    <OutputField value={file?.name ?? "..."} />

    <div class="mt-2">
        <SimpleButton
            text="Voeg toe"
            bgColor="#FFF"
            textColor="#0C3966"
            onClick={handleVoegToe}
        />
    </div>
</div>
