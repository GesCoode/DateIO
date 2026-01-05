<script lang="ts">
    import AlgemeneInformatieSymbol from "$lib/assets/AlgemeneInformatieSymbol0.svg";
    import MedischeInformatieSymbol from "$lib/assets/MedischeInformatieSymbol0.svg";
    import MedicatieSymbol from "$lib/assets/MedicatieSymbol0.svg";
    import AllergieenSymbol from "$lib/assets/AllergieenSymbol0.svg";
    import HuisartsSymbol from "$lib/assets/HuisartsSymbol0.svg";
    import ApotheekSymbol from "$lib/assets/ApotheekSymbol0.svg";
    import ContactPersonenSymbol from "$lib/assets/ContactPersonenSymbol0.svg";

    import AlgemeneInformatieData from "$lib/components/medisch/AlgemeneInformatieData.svelte";
    import MedischeInformatieData from "$lib/components/medisch/MedischeInformatieData.svelte";
    import MedicatieData from "$lib/components/medisch/MedicatieData.svelte";
    import AllergieenData from "$lib/components/medisch/AllergieenData.svelte";
    import HuisartsData from "$lib/components/medisch/HuisartsData.svelte";
    import ApotheekData from "$lib/components/medisch/ApotheekData.svelte";
    import ContactPersonenData from "$lib/components/medisch/ContactPersonenData.svelte";

    import InfoBox from "$lib/components/medisch/InfoBox.svelte";
</script>

<!-- Outer container defines relative positioning -->
<div class="flex flex-col md:flex-row w-full relative">
    <!-- Left block -->
    <div class="flex flex-col items-start gap-3 flex-1 px-5">
        <InfoBox
            icon={AlgemeneInformatieSymbol}
            header="Algemene Informatie"
            subheader="basisInformatie"
        >
            <div
                class="flex flex-col gap-4 px-4 py-2 bg-gray-50 rounded-b-[4px]"
            >
                <AlgemeneInformatieData />
            </div>
        </InfoBox>

        <InfoBox
            icon={MedischeInformatieSymbol}
            header="Medische Informatie"
            subheader="belangrijke aandoeningen/operaties"
        >
            <div
                class="flex flex-col gap-4 px-4 py-2 bg-gray-50 rounded-b-[4px]"
            >
                <MedischeInformatieData />
            </div>
        </InfoBox>

        <InfoBox
            icon={MedicatieSymbol}
            header="Medicatie"
            subheader="huidige medicijnen en doseringen"
        >
            <div
                class="flex flex-col gap-4 px-4 py-2 bg-gray-50 rounded-b-[4px]"
            >
                <MedicatieData />
            </div>
        </InfoBox>

        <InfoBox
            icon={AllergieenSymbol}
            header="Allergieën"
            subheader="bekende allergieën"
        >
            <div
                class="flex flex-col gap-4 px-4 py-2 bg-gray-50 rounded-b-[4px]"
            >
                <AllergieenData />
            </div>
        </InfoBox>
    </div>

    <!-- Divider -->
    <div
        class="hidden md:block absolute md:left-1/2 md:transform md:-translate-x-1/2 top-0 bottom-0 w-px bg-gray-300"
    ></div>

    <!-- Right block -->
    <div class="flex flex-col items-start gap-3 flex-1 px-5 mt-6 md:mt-0">
        <InfoBox
            icon={HuisartsSymbol}
            header="Huisarts"
            subheader="Contactgegevens huisarts"
        >
            <div
                class="flex flex-col gap-4 px-4 py-2 bg-gray-50 rounded-b-[4px]"
            >
                <HuisartsData />
            </div>
        </InfoBox>

        <InfoBox
            icon={ApotheekSymbol}
            header="Apotheek"
            subheader="Contactgegevens apotheek"
        >
            <div
                class="flex flex-col gap-4 px-4 py-2 bg-gray-50 rounded-b-[4px]"
            >
                <ApotheekData />
            </div>
        </InfoBox>

        <InfoBox
            icon={ContactPersonenSymbol}
            header="ICE-contactpersonen"
            subheader="personen bij nood"
        >
            <div
                class="flex flex-col gap-4 px-4 py-2 bg-gray-50 rounded-b-[4px]"
            >
                <ContactPersonenData />
            </div>
        </InfoBox>
    </div>
</div>
