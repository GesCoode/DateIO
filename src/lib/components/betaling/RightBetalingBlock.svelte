<script lang="ts">
    import SimpleButton from "../form/SimpleButton.svelte";

    type Payment = {
        datum: string;
        bedrag: string;
        betaalmethode: string;
        status: string;
    };

    export let handlePDF: () => void = () => {};

    // Temp data
    let payments: Payment[] = [
        {
            datum: "01-01-2026",
            bedrag: "€50,00",
            betaalmethode: "iDEAL",
            status: "Voltooid",
        },
        {
            datum: "15-01-2026",
            bedrag: "€75,00",
            betaalmethode: "Mollie",
            status: "Voltooid",
        },
        {
            datum: "01-01-2026",
            bedrag: "€50,00",
            betaalmethode: "iDEAL",
            status: "Voltooid",
        },
        {
            datum: "15-01-2026",
            bedrag: "€75,00",
            betaalmethode: "Mollie",
            status: "Voltooid",
        },
        {
            datum: "01-01-2026",
            bedrag: "€50,00",
            betaalmethode: "iDEAL",
            status: "Voltooid",
        },
        {
            datum: "15-01-2026",
            bedrag: "€75,00",
            betaalmethode: "Mollie",
            status: "Voltooid",
        },
        {
            datum: "01-01-2026",
            bedrag: "€50,00",
            betaalmethode: "iDEAL",
            status: "Voltooid",
        },
        {
            datum: "15-01-2026",
            bedrag: "€75,00",
            betaalmethode: "Mollie",
            status: "Voltooid",
        },
        {
            datum: "01-01-2026",
            bedrag: "€50,00",
            betaalmethode: "iDEAL",
            status: "Voltooid",
        },
        {
            datum: "15-01-2026",
            bedrag: "€75,00",
            betaalmethode: "Mollie",
            status: "Voltooid",
        },
        {
            datum: "01-01-2026",
            bedrag: "€50,00",
            betaalmethode: "iDEAL",
            status: "Voltooid",
        },
        {
            datum: "15-01-2026",
            bedrag: "€75,00",
            betaalmethode: "Mollie",
            status: "Voltooid",
        },
        {
            datum: "01-01-2026",
            bedrag: "€50,00",
            betaalmethode: "iDEAL",
            status: "Voltooid",
        },
        {
            datum: "15-01-2026",
            bedrag: "€75,00",
            betaalmethode: "Mollie",
            status: "Voltooid",
        },
    ];
</script>

<div class="flex flex-col h-full bg-[#FFF] p-4 rounded gap-4">
    <!-- Header -->
    <div class="text-black font-spaceGrotesk text-[20px] font-bold">
        Betalingsoverzicht
    </div>

    <!-- Payment list with headers -->
    <div class="flex flex-col overflow-y-auto">
        <!-- Column headers -->
        <div
            class="flex flex-row justify-between items-center bg-[#E0E0E0] rounded-t px-3 py-2 sticky top-0 z-10"
        >
            <div class="text-black font-bold w-1/5">Datum</div>
            <div class="text-black font-bold w-1/5">Bedrag</div>
            <div class="text-black font-bold w-1/5">Methode</div>
            <div class="text-black font-bold w-1/5">Status</div>
            <div class="text-black font-bold w-1/5 text-center">PDF</div>
        </div>

        <!-- Payment rows -->
        {#each payments as payment}
            <div
                class="flex flex-row justify-between items-center bg-[#F0F0F0] even:bg-[#FFF] rounded px-3 py-2"
            >
                <div class="text-black font-light w-1/5">{payment.datum}</div>
                <div class="text-black font-light w-1/5">{payment.bedrag}</div>
                <div class="text-black font-light w-1/5">
                    {payment.betaalmethode}
                </div>
                <div class="text-black font-light w-1/5">{payment.status}</div>
                <div class="flex justify-center w-1/5">
                    <div class="flex flex-col items-start">
                        <SimpleButton
                            text="PDF"
                            bgColor="#0C6639"
                            textColor="#FFF"
                            rounded={true}
                            onClick={handlePDF}
                        />
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>
