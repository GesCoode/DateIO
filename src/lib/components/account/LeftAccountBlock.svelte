<script lang="ts">
    import LabeledInput from "$lib/components/form/LabeledInput.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";
    import LabeledSliderInfo from "$lib/components/composits/LabeledSliderInfo.svelte";

    export let nieuwWachtwoord = "";
    export let herhaalNieuwWachtwoord = "";
    export let deactiveerAccount: boolean = false;

    export let handleChangePassword: () => void = () => {};
    export let handleVerwijderAccount: () => void = () => {};
</script>

<div class="flex h-full flex-1 justify-center items-center bg-white">
    <div class="flex flex-col items-start gap-3 w-[238px]">
        <!-- Nieuw Wachtwoord -->
        <LabeledInput
            id="nieuwWachtwoord"
            label="Uw nieuw wachtwoord"
            placeholder="Type nieuw wachtwoord"
            bind:value={nieuwWachtwoord}
        />

        <!-- Herhaal nieuw wachtwoord -->
        <LabeledInput
            id="herhaalNieuwWachtwoord"
            label="Herhaal uw nieuw wachtwoord"
            placeholder="Type nieuw wachtwoord"
            bind:value={herhaalNieuwWachtwoord}
        />

        <!-- Reset wachtwoord -->
        <SimpleButton
            text="Reset uw wachtwoord"
            bgColor="#0C3966"
            textColor="#FFF"
            onClick={handleChangePassword}
        />

        <!-- Spacer -->
        <div style="height: 12px;"></div>

        <!-- Deactiveer account -->
        <LabeledSliderInfo
            label="Deactiveer uw account"
            tooltipText="Deactiveer tijdelijk uw account. U kunt deze deactivatie ieder moment weer terugzetten."
            statusTextTrue="U account is gedeactiveerd"
            statusTextFalse="U account is geactiveerd"
            bind:checked={deactiveerAccount}
            handleColor="#FFF"
            trueColor="#E30613"
            statusTextColor="#374151"
        />

        <!-- Verwijder account -->
        <div class="flex flex-col items-start gap-1">
            <h2 class="text-sm font-medium text-gray-700">
                Verwijder uw account
            </h2>
            <SimpleButton
                text="Verwijder uw account"
                bgColor="#DAA9A9"
                textColor="#0C3966"
                onClick={handleVerwijderAccount}
            />
        </div>
    </div>
</div>
