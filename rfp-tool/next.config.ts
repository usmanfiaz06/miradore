import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/miradore",
  assetPrefix: "/miradore/",
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
