<script lang="ts">
    import SimpleButton from "../form/SimpleButton.svelte";
    import EditPopUp from "./editPopUp.svelte";
    import BewerkPopUp from "./editPopUp.svelte";

    type Payment = {
        aanmaakdatum: string;
        omschrijving: string;
        soscode: string;
        status: string;
    };

    let payments: Payment[] = [
        {
            aanmaakdatum: "01-01-2026",
            omschrijving: "Eerste armband",
            soscode: "RF1I65YZ2",
            status: "Actief",
        },
        {
            aanmaakdatum: "15-01-2026",
            omschrijving: "Tweede armband",
            soscode: "AB12CD34",
            status: "Inactief",
        },

        {
            aanmaakdatum: "01-01-2026",
            omschrijving: "Eerste armband",
            soscode: "RF1I65YZ2",
            status: "Actief",
        },
        {
            aanmaakdatum: "15-01-2026",
            omschrijving: "Tweede armband",
            soscode: "AB12CD34",
            status: "Inactief",
        },

        {
            aanmaakdatum: "01-01-2026",
            omschrijving: "Eerste armband",
            soscode: "RF1I65YZ2",
            status: "Actief",
        },
        {
            aanmaakdatum: "15-01-2026",
            omschrijving: "Tweede armband",
            soscode: "AB12CD34",
            status: "Inactief",
        },

        {
            aanmaakdatum: "01-01-2026",
            omschrijving: "Eerste armband",
            soscode: "RF1I65YZ2",
            status: "Actief",
        },
        {
            aanmaakdatum: "15-01-2026",
            omschrijving: "Tweede armband",
            soscode: "AB12CD34",
            status: "Inactief",
        },
    ];

    let showPopUp = false;
    let selectedPaymentIndex: number | null = null;

    function openPopUp(index: number) {
        selectedPaymentIndex = index;
        showPopUp = true;
    }

    function closePopUp() {
        showPopUp = false;
        selectedPaymentIndex = null;
    }
</script>

<div class="flex flex-col h-full bg-[#FFF] p-4 rounded gap-4">
    <div class="text-black font-spaceGrotesk text-[20px] font-bold">
        Mijn SOStags
    </div>

    <div class="flex flex-col overflow-y-auto">
        <!-- Column headers -->
        <div
            class="flex flex-row justify-between items-center bg-[#E0E0E0] rounded-t px-3 py-2 sticky top-0 z-10"
        >
            <div class="text-black font-bold w-1/5">Datum</div>
            <div class="text-black font-bold w-1/5">Bedrag</div>
            <div class="text-black font-bold w-1/5">Methode</div>
            <div class="text-black font-bold w-1/5">Status</div>
            <div class="text-black font-bold w-1/5 text-center">
                Bewerk SOStag
            </div>
        </div>

        {#each payments as payment, index}
            <div
                class="flex flex-row justify-between items-center bg-[#F0F0F0] even:bg-[#FFF] rounded px-3 py-2"
            >
                <div class="text-black font-light w-1/5">
                    {payment.aanmaakdatum}
                </div>
                <div class="text-black font-light w-1/5">
                    {payment.omschrijving}
                </div>
                <div class="text-black font-light w-1/5">{payment.soscode}</div>
                <div
                    class="text-black font-light w-1/5 flex items-center gap-2"
                >
                    <span
                        class="w-3 h-3 rounded-full"
                        style="background-color: {payment.status === 'Actief'
                            ? 'green'
                            : 'red'}"
                    ></span>
                    {payment.status}
                </div>
                <div class="w-1/5 flex justify-center">
                    <div class="flex flex-col items-start">
                        <SimpleButton
                            text="bewerk"
                            bgColor="#0C3966"
                            textColor="#FFF"
                            rounded={true}
                            on:click={() => openPopUp(index)}
                        />
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>

<EditPopUp></EditPopUp>
