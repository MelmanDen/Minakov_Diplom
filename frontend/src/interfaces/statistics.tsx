import { VirusTotalResponse } from "./virus_total_response";
import { CheckphishResponse } from "./checkphish_response";

export type Statistics = {
  checkPhish: CheckphishResponse | null;
  virusTotal: VirusTotalResponse | null;
};