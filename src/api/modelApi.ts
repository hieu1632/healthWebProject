// src/api/modelApi.ts
export type FeaturesResponse = {
  features: string[];
  symptom_meta?: Record<string, any>;
  advice?: Record<string, any>;
};

export type PredictResponse = {
  predictions?: Array<{
    disease: string;
    prob: number;
    severity?: string;
    urgency?: string;
  }>;
  alertPresent?: boolean;
  symptom_meta?: Record<string, any>;
};

const ENV_BASE = import.meta.env.VITE_API_BASE as string | undefined;

// thử danh sách endpoint khả dĩ
const CANDIDATES = [
  ENV_BASE,
  "http://localhost:8000",
  "http://127.0.0.1:8000",
  "http://localhost:5000",
  "http://127.0.0.1:5000",
].filter(Boolean) as string[];

async function tryFetchJson(url: string) {
  const res = await fetch(url, { method: "GET" });
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch (e) {
    throw new Error(`Invalid JSON from ${url}. Status ${res.status}. Body: ${text}`);
  }
  if (!res.ok)
    throw new Error(
      `HTTP ${res.status} from ${url} - ${JSON.stringify(json).slice(0, 200)}`
    );
  return json;
}

export async function getModelFeatures(): Promise<FeaturesResponse> {
  const paths = [
    "/model/features",
    "/api/model/features",
    "/api/products/type",
    "/model/features/",
  ];
  let lastErr: Error | null = null;

  for (const base of CANDIDATES) {
    for (const p of paths) {
      const url = `${base.replace(/\/+$/, "")}${p.startsWith("/") ? p : "/" + p}`;
      try {
        const json = await tryFetchJson(url);
        console.log(
          "[modelApi] success fetch",
          url,
          json && Object.keys(json).slice(0, 10)
        );
        // Chuẩn hóa dữ liệu trả về
        return {
          features: json.features || json.data?.features || json || [],
          symptom_meta: json.symptom_meta || json.symptomMeta || {},
        } as FeaturesResponse;
      } catch (err: unknown) {
        if (err instanceof Error) {
          lastErr = err;
          console.warn(
            "[modelApi] fetch fail",
            url,
            err.message?.slice?.(0, 200) || err
          );
        } else {
          console.warn("[modelApi] fetch fail", url, err);
        }
        // thử endpoint tiếp theo
      }
    }
  }
  throw new Error(
    "All candidate endpoints failed. Last error: " + (lastErr?.message || lastErr)
  );
}

export async function predictApi(
  symptoms: string[],
  topK = 5
): Promise<PredictResponse> {
  const payload = { symptoms, topK };
  let lastErr: Error | null = null;

  for (const base of CANDIDATES) {
    const url = `${base.replace(/\/+$/, "")}/predict`;
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const json = await res.json();
      if (!res.ok)
        throw new Error(
          `HTTP ${res.status} - ${JSON.stringify(json).slice(0, 200)}`
        );
      return json as PredictResponse;
    } catch (err: unknown) {
      if (err instanceof Error) {
        lastErr = err;
        console.warn(
          "[modelApi] predict fail",
          url,
          err.message?.slice?.(0, 200) || err
        );
      } else {
        console.warn("[modelApi] predict fail", url, err);
      }
    }
  }

  throw new Error(
    "Predict failed on all candidates. Last: " + (lastErr?.message || lastErr)
  );
}
