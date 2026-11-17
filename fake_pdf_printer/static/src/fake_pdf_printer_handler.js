import { downloadFile } from "@web/core/network/download";
import { registry } from "@web/core/registry";

// "Prints" each PDF job by downloading it, named after the selected printer
registry.category("printer.type.handlers").add("fake_pdf", async (printer, duplex, jobs) => {
    for (const job of jobs.filter((job) => job.type === "fake_pdf")) {
        console.log(`[fake_pdf] job for printer "${printer.name}" (duplex: ${duplex})`);
        await downloadFile(
            `data:application/pdf;base64,${job.report}`,
            `fake_printer_${printer.name}_${Date.now()}.pdf`,
            "application/pdf"
        );
    }
});
