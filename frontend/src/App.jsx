import { useEffect, useState } from "react";
import "./App.css";


function App() {

  const [file, setFile] = useState(null);

const [packetSize, setPacketSize] = useState(30);

const [lossRate, setLossRate] = useState(20);

const [timeout, setTimeoutValue] = useState(0.01);

const [result, setResult] = useState(null);

const [loading, setLoading] = useState(false);

const [currentEventIndex, setCurrentEventIndex] = useState(-1);

const [isSimulating, setIsSimulating] = useState(false);
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };


  const handleTransfer = async () => {

    if (!file) {
      alert("Please select a file first.");
      return;
    }

    setLoading(true);
    setResult(null);

    const formData = new FormData();

    formData.append("file", file);
    formData.append("loss_rate", lossRate / 100);
    formData.append("packet_size", packetSize);
    formData.append("timeout", timeout);


    try {

      const response = await fetch(
        "https://resilientfiletransfer.onrender.com/transfer/stop-and-wait",
        {
          method: "POST",
          body: formData
        }
      );


      const data = await response.json();

      setResult(data);

    } catch (error) {

      console.error(error);

      alert(
        "Could not connect to the backend."
      );

    } finally {

      setLoading(false);

    }
  };

useEffect(() => {

  if (
    !result ||
    !result.transfer_log ||
    result.transfer_log.length === 0
  ) {
    return;
  }

  setCurrentEventIndex(0);
  setIsSimulating(true);

  const interval = setInterval(() => {

    setCurrentEventIndex((previousIndex) => {

      const nextIndex = previousIndex + 1;

      if (nextIndex >= result.transfer_log.length) {

        clearInterval(interval);

        setIsSimulating(false);

        return previousIndex;
      }

      return nextIndex;

    });

  }, 700);

  return () => {
    clearInterval(interval);
  };

}, [result]);
  const getEventLabel = (event) => {

    const labels = {

      DATA_SENT: "Data packet sent",

      DATA_RECEIVED: "Data packet received",

      DATA_LOST: "Data packet lost",

      ACK_GENERATED: "ACK generated",

      ACK_RECEIVED: "ACK received",

      ACK_LOST: "ACK lost",

      TIMEOUT: "Timeout",

      RETRANSMISSION: "Retransmission",

      DUPLICATE_RECEIVED: "Duplicate packet received"

    };

    return labels[event] || event;
  };


  const getEventClass = (event) => {

    if (
      event === "DATA_LOST" ||
      event === "ACK_LOST"
    ) {
      return "event lost";
    }

    if (
      event === "TIMEOUT" ||
      event === "RETRANSMISSION" ||
      event === "DUPLICATE_RECEIVED"
    ) {
      return "event warning";
    }

    if (
      event === "ACK_RECEIVED" ||
      event === "DATA_RECEIVED"
    ) {
      return "event success";
    }

    return "event";
  };

  const getNetworkStatus = () => {

    if (!result || !result.transfer_log) {
      return "Waiting for transfer";
    }

    const lostEvents = result.transfer_log.filter(
      (log) =>
        log.event === "DATA_LOST" ||
        log.event === "ACK_LOST"
    );

    const retransmissionEvents = result.transfer_log.filter(
      (log) =>
        log.event === "RETRANSMISSION"
    );

    if (retransmissionEvents.length > 0) {
      return "Unreliable network detected packet loss";
    }

    if (lostEvents.length > 0) {
      return "Packet loss detected";
    }

    return "All packets delivered successfully";
     
  };
  const getSimulationClass = () => {

    if (
      !result ||
      !result.transfer_log ||
      currentEventIndex < 0 ||
      currentEventIndex >= result.transfer_log.length
    ) {
      return "";
    }

    const event = result.transfer_log[currentEventIndex].event;

    if (
      event === "DATA_SENT" ||
      event === "RETRANSMISSION"
    ) {
      return "moving-packet data-forward";
    }

    if (
      event === "DATA_RECEIVED"
    ) {
      return "moving-packet data-arrived";
    }

    if (
      event === "ACK_GENERATED"
    ) {
      return "moving-packet ack-start";
    }

    if (
      event === "ACK_RECEIVED"
    ) {
      return "moving-packet ack-back";
    }

    if (
      event === "DATA_LOST"
    ) {
      return "moving-packet data-lost";
    }

    if (
      event === "ACK_LOST"
    ) {
      return "moving-packet ack-lost";
    }

    return "";
  };
  
  return (

    <div className="app">

      <header>

        <h1>
          Resilient File Transfer
        </h1>

        <p>
          Reliable file transfer over an unreliable network
        </p>

      </header>


      <main>

        <section className="card">

          <h2>Transfer Configuration</h2>


          <label>
            Select File
          </label>

          <input
            type="file"
            onChange={handleFileChange}
          />


         <label>
  Protocol
</label>

<div className="protocol-display">
  Stop-and-Wait ARQ
</div>


          <label>
            Packet Size (bytes)
          </label>

          <input
            type="number"
            min="1"
            value={packetSize}
            onChange={(event) =>
              setPacketSize(event.target.value)
            }
          />


          <label>
            Loss Rate (%)
          </label>

          <input
            type="number"
            min="0"
            max="100"
            value={lossRate}
            onChange={(event) =>
              setLossRate(event.target.value)
            }
          />


          <label>
            Timeout (seconds)
          </label>

          <input
            type="number"
            step="0.01"
            min="0"
            value={timeout}
            onChange={(event) =>
              setTimeoutValue(event.target.value)
            }
          />


          <button
            onClick={handleTransfer}
            disabled={loading}
          >

            {loading
              ? "Transferring..."
              : "Start Transfer"
            }

          </button>

        </section>

            <section className="card">

              <h2>Network Flow</h2>
{result &&
  result.transfer_log &&
  currentEventIndex >= 0 &&
  currentEventIndex < result.transfer_log.length && (

    <div className="simulation-status">

      <strong>
        Packet {result.transfer_log[currentEventIndex].sequence_number}
      </strong>

      <span>
        {getEventLabel(
          result.transfer_log[currentEventIndex].event
        )}
      </span>

    </div>

)}
              <div className="network-flow">
<div
  key={currentEventIndex}
  className={getSimulationClass()}
>
  {result &&
    result.transfer_log &&
    currentEventIndex >= 0 &&
    currentEventIndex < result.transfer_log.length && (
      <>
        {result.transfer_log[currentEventIndex].event.includes("ACK")
          ? "ACK"
          : "●"}
      </>
    )}
</div>
                <div className="network-node">

                  <div className="node-icon">
                    S
                  </div>

                  <h3>Sender</h3>

                  <p>
                    File packets
                  </p>

                </div>


                <div className="network-connection">

                  <div className="connection-line">
                    →
                  </div>

                  <span>
                    DATA
                  </span>

                </div>


                <div className="network-node network">

                  <div className="node-icon">
                    N
                  </div>

                  <h3>Unreliable Network</h3>

                  <p>
                    Loss Rate: {lossRate}%
                  </p>

                </div>


                <div className="network-connection">

                  <div className="connection-line">
                    →
                  </div>

                  <span>
                    DATA
                  </span>

                </div>


                <div className="network-node">

                  <div className="node-icon">
                    R
                  </div>

                  <h3>Receiver</h3>

                  <p>
                    File reassembly
                  </p>

                </div>

              </div>


              <div className="network-status">

                <strong>
                  Network Status:
                </strong>

                <span>
                  {getNetworkStatus()}
                </span>

              </div>


              <div className="ack-flow">

                <span>
                  Receiver
                </span>

                <span className="ack-arrow">
                  ← ACK
                </span>

                <span>
                  Sender
                </span>

              </div>

            </section>
        {result && (

          <>

            <section className="card">

              <h2>Transfer Results</h2>


              <div className="results">

                <div>
                  <span>File</span>

                  <strong>
                    {result.filename}
                  </strong>
                </div>


                <div>
                  <span>Packets</span>

                  <strong>
                    {result.total_packets}
                  </strong>
                </div>


                <div>
                  <span>Transmissions</span>

                  <strong>
                    {result.total_transmissions}
                  </strong>
                </div>


                <div>
                  <span>Retransmissions</span>

                  <strong>
                    {result.retransmissions}
                  </strong>
                </div>


                <div>
                  <span>Duplicates</span>

                  <strong>
                    {result.duplicate_packets}
                  </strong>
                </div>


                <div>
                  <span>Completion Time</span>

                  <strong>
                    {result.completion_time_seconds} s
                  </strong>
                </div>

              </div>


              <div className="integrity">

                File Integrity:

                <strong>
                  {result.file_integrity}
                </strong>

              </div>

            </section>


            <section className="card">

              <h2>Packet Activity</h2>

              <div className="activity">



                {result.transfer_log.map(
                  (log, index) => (

                    <div
                      className={getEventClass(log.event)}
                      key={index}
                    >

                      <span className="event-number">
                        #{index + 1}
                      </span>

                      <span className="packet-number">
                        Packet {log.sequence_number}
                      </span>

                      <span className="event-label">
                        {getEventLabel(log.event)}
                      </span>

                    </div>

                  )
                )}

              </div>

            </section>

          </>

        )}

      </main>

    </div>

  );
}


export default App;