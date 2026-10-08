from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from transfer.file_splitter import split_file
from transfer.reassembler import reassemble_file
from transfer.stop_and_wait import stop_and_wait_transfer


app = FastAPI(
    title="Resilient File Transfer",
    description="Reliable file transfer over an unreliable packet-switched network",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
   allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Resilient File Transfer API is running"
    }


@app.post("/transfer/stop-and-wait")
async def stop_and_wait(
    file: UploadFile = File(...),
    loss_rate: float = Form(0.2),
    packet_size: int = Form(30),
    timeout: float = Form(0.01)
):

    # Validate loss rate
    if loss_rate < 0 or loss_rate > 1:
        return {
            "status": "error",
            "message": "loss_rate must be between 0 and 1"
        }

    # Validate packet size
    if packet_size <= 0:
        return {
            "status": "error",
            "message": "packet_size must be greater than 0"
        }

    # Read uploaded file
    file_data = await file.read()

    # Create temporary input file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix="_input"
    ) as temp_input:

        temp_input.write(file_data)
        input_path = temp_input.name

    try:

        # Split file into packets
        packets = split_file(
            input_path,
            packet_size=packet_size
        )

        # Run Stop-and-Wait protocol
        result = stop_and_wait_transfer(
            packets,
            loss_rate=loss_rate,
            timeout=timeout
        )

        # Create temporary reconstructed file
        reconstructed_path = input_path + "_reconstructed"

        # Reassemble received packets
        reassemble_file(
            result["received_packets"],
            reconstructed_path
        )

        # Verify file integrity
        with open(input_path, "rb") as original:
            original_data = original.read()

        with open(reconstructed_path, "rb") as reconstructed:
            reconstructed_data = reconstructed.read()

        integrity = (
            original_data == reconstructed_data
        )

        return {
            "status": "success",
            "filename": file.filename,
            "file_size_bytes": len(file_data),
            "packet_size_bytes": packet_size,
            "total_packets": len(packets),
            "loss_rate": loss_rate,
            "total_transmissions": result["total_transmissions"],
            "retransmissions": result["retransmissions"],
            "duplicate_packets": result["duplicate_packets"],
            "completion_time_seconds": round(
                result["completion_time"],
                4
            ),
            "file_integrity": (
                "PASS" if integrity else "FAIL"
            ),
            "transfer_log": result["transfer_log"]
        }
    finally:

        # Remove temporary files
        if os.path.exists(input_path):
            os.remove(input_path)

        if os.path.exists(input_path + "_reconstructed"):
            os.remove(input_path + "_reconstructed")