import type { KeycloakTokenSet, NextAuthOptions } from "next-auth";
import type { JWT } from "next-auth/jwt";
import KeycloakProvider from "next-auth/providers/keycloak";

const keycloak = KeycloakProvider({
  id: "keycloak",
  clientId: process.env.KEYCLOAK_CLIENT_ID as string,
  clientSecret: process.env.KEYCLOAK_CLIENT_SECRET as string,
  issuer: process.env.KEYCLOAK_ISSUER,
  authorization: { params: { scope: "openid email profile offline_access" } },
});

// this performs the final handshake for the keycloak provider
async function doFinalSignoutHandshake(token: JWT) {
  if (token.provider == keycloak.id) {
    try {
      const issuerUrl = keycloak.options?.issuer;
      const logOutUrl = new URL(`${issuerUrl}/protocol/openid-connect/logout`);
      logOutUrl.searchParams.set("id_token_hint", token.id_token);
      const { status, statusText } = await fetch(logOutUrl);
      console.log("Completed post-logout handshake", status, statusText);
    } catch (e: any) {
      console.error("Unable to perform post-logout handshake", e?.code || e);
    }
  }
}

async function refreshAccessToken(token: JWT): Promise<JWT> {
  try {
    const response = await fetch(`${keycloak.options?.issuer}/protocol/openid-connect/token`, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: keycloak.options?.clientId as string,
        client_secret: keycloak.options?.clientSecret as string,
        grant_type: "refresh_token",
        refresh_token: token.refresh_token as string,
      }),
      method: "POST",
    });

    const tokensRaw = await response.json();
    const tokens: KeycloakTokenSet = tokensRaw;
    if (!response.ok) throw tokens;

    const expiresAt = Math.floor(Date.now() / 1000 + tokens.expires_in);
    console.log(
      `Token was refreshed. New token expires in ${tokens.expires_in} sec at ${expiresAt}, refresh token expires in ${tokens.refresh_expires_in} sec`
    );
    const newToken: JWT = {
      ...token,
      access_token: tokens.access_token,
      expires_at: expiresAt,
      refresh_token: tokens.refresh_token ?? token.refresh_token,
      id_token: tokens.id_token ?? token.id_token,
      provider: keycloak.id,
    };
    return newToken;
  } catch (error) {
    console.error("Error refreshing access token: ", error);
    return {
      ...token,
      error: "RefreshAccessTokenError",
    };
  }
}

export const options: NextAuthOptions = {
  secret: process.env.NEXTAUTH_SECRET,
  providers: [keycloak],
  pages: {
    signIn: "/auth/login",
    error: "/auth/error",
  },
  theme: {
    colorScheme: "light",
  },
  callbacks: {
    async session({ session, token }) {
      console.log(`Executing session() with token ${token.expires_at}`);
      if (token) {
        session.access_token = token.access_token;
      }
      session.error = token.error;
      return session;
    },
    async jwt({ token, account, user }) {
      console.log("Executing jwt()");
      if (account && user) {
        // The account and user will be available on first sign in with this provider
        if (!account.access_token) throw Error("Auth Provider missing access token");
        if (!account.refresh_token) throw Error("Auth Provider missing refresh token");
        if (!account.id_token) throw Error("Auth Provider missing ID token");
        // Save the access token and refresh token in the JWT on the initial login
        const newToken: JWT = {
          ...token,
          access_token: account.access_token,
          refresh_token: account.refresh_token,
          id_token: account.id_token,
          expires_at: Math.floor(account.expires_at ?? 0),
          provider: account.provider,
        };
        return newToken;
      }
      // Return previous token if the access token has not expired yet
      if (Date.now() < token.expires_at * 1000) {
        // If the access token has not expired yet, return it
        console.log("token is valid");
        return token;
      }
      // If the access token has expired, try to refresh it
      console.log(`\n>>> Old token expired: ${token.expires_at}`);
      const newToken = await refreshAccessToken(token);
      console.log(`New token acquired: ${newToken.expires_at}`);
      return newToken;
    },
  },
  events: {
    signOut: async ({ token }) => doFinalSignoutHandshake(token),
  },
  jwt: {
    maxAge: 1 * 60, // 1 minute, same as in Keycloak
  },
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days : 2592000, same as in Keycloak
  },
};
