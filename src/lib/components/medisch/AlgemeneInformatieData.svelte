<script lang="ts">
    import LabeledInput from "$lib/components/form/LabeledInput.svelte";
    import LabeledSliderInfo from "$lib/components/composits/LabeledSliderInfo.svelte";
    import ResizableTextarea from "$lib/components/form/ResizableTextarea.svelte";
    import SimpleButton from "$lib/components/form/SimpleButton.svelte";

    export let handleOpslaan: () => void = () => {};

    export let bloedGroep = "";

    export let reanimatieWens: boolean = false;
    export let donor: boolean = false;
    export let contactLenzen: boolean = false;
    export let gehoorApparaat: boolean = false;
    export let bril: boolean = false;
    export let gebitOfElementen: boolean = false;
</script>

<!-- Bloedgroep -->
<LabeledInput
    id="Bloedgroep"
    label="Uw bloedgroep"
    placeholder="A+/A-/B+/B-/AB+/AB-/O+/O-"
    bind:value={bloedGroep}
    tooltipText="De voorkeur gaat uit naar de Rh Factor systeem."
    showTooltip={true}
/>

<!-- Prothese -->
<ResizableTextarea
    id="Protheses"
    label="Protheses"
    placeholder="Uw protheses"
    tooltipText="Kunstmatige vervanging van een lichaamsdeel, bijvoorbeeld een arm-, been- of oogprothese."
/>

<!-- Reanimatie wens -->
<LabeledSliderInfo
    label="Reanimatie wens"
    tooltipText="Geef hier aan of u in geval van een hartstilstand gereanimeerd wilt worden of niet."
    statusTextTrue="Wel reanimeren"
    statusTextFalse="Niet reanimeren"
    bind:checked={reanimatieWens}
    handleColor="#FFF"
    trueColor="#45B652"
    statusTextColor="#374151"
/>

<!-- Donor -->
<LabeledSliderInfo
    label="Orgaandonor"
    tooltipText=""
    statusTextTrue="Ik ben wel orgaandonor"
    statusTextFalse="Ik ben geen orgaandonor"
    bind:checked={donor}
    handleColor="#FFF"
    trueColor="#45B652"
    statusTextColor="#374151"
    showTooltip={false}
/>

<!-- Contactlenzen -->
<LabeledSliderInfo
    label="Contactlenzen"
    tooltipText=""
    statusTextTrue="Ik draag wel contactlenzen"
    statusTextFalse="Ik draag geen contactlenzen"
    bind:checked={contactLenzen}
    handleColor="#FFF"
    trueColor="#45B652"
    statusTextColor="#374151"
    showTooltip={false}
/>

<!-- Gehoorapparaat -->
<LabeledSliderInfo
    label="Gehoorapparaat"
    tooltipText=""
    statusTextTrue="Ik draag wel een gehoorapparaat"
    statusTextFalse="Ik draag geen gehoorapparaat"
    bind:checked={gehoorApparaat}
    handleColor="#FFF"
    trueColor="#45B652"
    statusTextColor="#374151"
    showTooltip={false}
/>

<!-- Bril -->
<LabeledSliderInfo
    label="Bril"
    tooltipText=""
    statusTextTrue="Ik draag wel een bril"
    statusTextFalse="Ik draag geen bril"
    bind:checked={bril}
    handleColor="#FFF"
    trueColor="#45B652"
    statusTextColor="#374151"
    showTooltip={false}
/>

<!-- Gebit/Elementen -->
<LabeledSliderInfo
    label="Gebit / Elementen"
    tooltipText="Vul hier in of u natuurlijke tanden of kunstmatige gebitselementen zoals kronen, bruggen of implantaten heeft."
    statusTextTrue="Ik heb wel een gebit of elementen"
    statusTextFalse="Ik heb geen gebit of elementen"
    bind:checked={gebitOfElementen}
    handleColor="#FFF"
    trueColor="#45B652"
    statusTextColor="#374151"
/>

<!-- Opslaan -->
<div class="flex flex-col items-start">
    <SimpleButton
        text="Opslaan"
        bgColor="#0C3966"
        textColor="#FFF"
        onClick={handleOpslaan}
    />
</div>
