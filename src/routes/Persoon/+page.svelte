<script lang="ts">
    import LabeledInput from "$lib/components/form/LabeledInput.svelte";
    import LabeledSliderInfo from "$lib/components/composits/LabeledSliderInfo.svelte";
    import ProfilePicture from "$lib/components/persoon/ProfilePicture.svelte";
    import FileManager from "$lib/components/composits/FileManager.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";
    import InformationBox from "$lib/components/form/InformationBox.svelte";

    export let voornaam = "";
    export let achternaam = "";
    export let roepnaam = "";
    export let adres = "";
    export let plaats = "";
    export let postcode = "";
    export let land = "";
    export let zorgVerzekeraar = "";
    export let polisNummer = "";

    export let adresZichtbaar: boolean = false;
    export let fotoZichtbaarheid: boolean = false;

    // Dynamic FileManager list
    let fileManagers: number[] = [0, 1, 2]; // start with 3
    let nextId = 3;
    let errorMessage: string = "";

    // Add a new FileManager
    function handleVermeldingToevoegen() {
        if (fileManagers.length >= 6) {
            errorMessage = "Er zijn maximaal 6 documenten toegestaan.";
            return;
        }
        fileManagers = [...fileManagers, nextId++];
        errorMessage = ""; // clear error on successful selection
    }

    // Remove a FileManager by index
    function verwijderBestand(index: number) {
        fileManagers = fileManagers.filter((_, i) => i !== index);
    }
</script>

<div class="flex flex-col lg:flex-row w-full gap-3 items-stretch">
    <!-- Left block -->
    <div class="flex flex-col lg:flex-row flex-1 gap-4">
        <!-- Profile picture -->
        <div
            class="flex flex-col gap-4 px-4 py-6 items-center w-full lg:w-[200px] order-1 lg:order-2"
        >
            <ProfilePicture bind:fotoZichtbaarheid />
        </div>

        <!-- Inputs -->
        <div class="flex flex-col gap-4 py-2 w-full order-2 lg:order-1">
            <!-- Persoonlijke gegevens -->
            <div class="flex w-full flex-row py-2 gap-4">
                <div class="flex flex-col gap-4 px-4 py-2 w-full">
                    <LabeledInput
                        id="Voornaam"
                        label="Voornaam"
                        placeholder="John"
                        bind:value={voornaam}
                        showTooltip={false}
                    />
                    <LabeledInput
                        id="Achternaam"
                        label="Achternaam"
                        placeholder="Doe"
                        bind:value={achternaam}
                        showTooltip={false}
                    />
                </div>
                <div
                    class="flex flex-col gap-4 px-4 py-2 w-full rounded-b-[4px]"
                >
                    <LabeledInput
                        id="Roepnaam"
                        label="Roepnaam"
                        placeholder=""
                        bind:value={roepnaam}
                        showTooltip={false}
                    />
                </div>
            </div>

            <hr class="border-t border-gray-200 w-full" />

            <!-- Adres -->
            <div class="flex w-full flex-row py-2 gap-4">
                <div class="flex flex-col gap-4 px-4 py-2 w-full">
                    <LabeledInput
                        id="Adres"
                        label="Adres"
                        placeholder=""
                        bind:value={adres}
                        showTooltip={false}
                    />
                    <LabeledInput
                        id="Plaats"
                        label="Plaats"
                        placeholder=""
                        bind:value={plaats}
                        showTooltip={false}
                    />
                    <LabeledSliderInfo
                        label="Adres zichtbaar bij scannen"
                        bind:checked={adresZichtbaar}
                        handleColor="#FFF"
                        trueColor="#45B652"
                        statusTextColor="#374151"
                        showTooltip={false}
                        statusTextTrue="Uw adres is wel zichtbaar"
                        statusTextFalse="Uw adres is niet zichtbaar"
                    />
                </div>
                <div class="flex flex-col gap-4 px-4 py-2 w-full">
                    <LabeledInput
                        id="Postcode"
                        label="Postcode"
                        placeholder=""
                        bind:value={postcode}
                        showTooltip={false}
                    />
                    <LabeledInput
                        id="Land"
                        label="Land"
                        placeholder=""
                        bind:value={land}
                        showTooltip={false}
                    />
                </div>
            </div>

            <hr class="border-t border-gray-200 w-full" />

            <!-- Zorgverzekeraar -->
            <div class="flex w-full flex-row py-2 gap-4">
                <div class="flex flex-col gap-4 px-4 py-2 w-full">
                    <LabeledInput
                        id="Zorgverzekeraar"
                        label="Zorgverzekeraar"
                        placeholder=""
                        bind:value={zorgVerzekeraar}
                        showTooltip={false}
                    />
                </div>
                <div class="flex flex-col gap-4 px-4 py-2 w-full">
                    <LabeledInput
                        id="Polisnummer"
                        label="Polisnummer"
                        placeholder=""
                        bind:value={polisNummer}
                        showTooltip={false}
                    />
                </div>
            </div>
        </div>
    </div>

    <!-- Right block -->
    <div class="flex flex-col gap-4 py-4 px-4 bg-[#0C3966] w-full lg:w-[30%]">
        {#each fileManagers as id, index (id)}
            <div class="flex flex-col w-full bg-[#0C3966] rounded">
                <!-- Label + cross -->
                <div class="flex justify-between items-center mb-1">
                    <span class="text-white font-medium"
                        >Bestand {index + 1}</span
                    >
                    <button
                        class="text-white font-bold px-2 rounded hover:bg-white/20"
                        on:click={() => verwijderBestand(index)}
                        aria-label="Verwijder bestand"
                    >
                        ✕
                    </button>
                </div>

                <!-- FileManager component -->
                <FileManager onError={(msg) => (errorMessage = msg)} />
            </div>
        {/each}

        {#if errorMessage}
            <div class="text-white text-sm mt-2">{errorMessage}</div>
        {/if}

        <!-- Division line -->
        <hr class="border-t border-gray-500 w-full" />

        <!-- Voeg extra bestand toe knop -->
        <div class="flex flex-col items-start mt-2">
            <SimpleButton
                text="Voeg extra bestand toe"
                bgColor="#FFF"
                textColor="#0C3966"
                onClick={handleVermeldingToevoegen}
            />
        </div>

        <!-- Uitleg -->
        <InformationBox>
            <ul class="list-disc list-inside space-y-1">
                <p>
                    Upload hier maximaal 6 medische documenten. Denk hierbij
                    aan:
                </p>
                <li>Wilsbeschikking</li>
                <li>Donorcodicil</li>
                <li>Medische dossiers</li>
            </ul>
        </InformationBox>
    </div>
</div>
