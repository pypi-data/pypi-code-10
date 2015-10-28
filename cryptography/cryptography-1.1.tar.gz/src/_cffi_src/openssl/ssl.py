# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import absolute_import, division, print_function

INCLUDES = """
#include <openssl/ssl.h>

typedef STACK_OF(SSL_CIPHER) Cryptography_STACK_OF_SSL_CIPHER;
"""

TYPES = """
/*
 * Internally invented symbols to tell which versions of SSL/TLS are supported.
*/
static const long Cryptography_HAS_SSL2;
static const long Cryptography_HAS_SSL3_METHOD;
static const long Cryptography_HAS_TLSv1_1;
static const long Cryptography_HAS_TLSv1_2;
static const long Cryptography_HAS_SECURE_RENEGOTIATION;
static const long Cryptography_HAS_COMPRESSION;
static const long Cryptography_HAS_TLSEXT_STATUS_REQ_CB;
static const long Cryptography_HAS_STATUS_REQ_OCSP_RESP;
static const long Cryptography_HAS_TLSEXT_STATUS_REQ_TYPE;
static const long Cryptography_HAS_GET_SERVER_TMP_KEY;
static const long Cryptography_HAS_SSL_CTX_SET_CLIENT_CERT_ENGINE;

/* Internally invented symbol to tell us if SNI is supported */
static const long Cryptography_HAS_TLSEXT_HOSTNAME;

/* Internally invented symbol to tell us if SSL_MODE_RELEASE_BUFFERS is
 * supported
 */
static const long Cryptography_HAS_RELEASE_BUFFERS;

/* Internally invented symbol to tell us if SSL_OP_NO_COMPRESSION is
 * supported
 */
static const long Cryptography_HAS_OP_NO_COMPRESSION;

static const long Cryptography_HAS_SSL_OP_MSIE_SSLV2_RSA_PADDING;
static const long Cryptography_HAS_SSL_SET_SSL_CTX;
static const long Cryptography_HAS_SSL_OP_NO_TICKET;
static const long Cryptography_HAS_NETBSD_D1_METH;
static const long Cryptography_HAS_NEXTPROTONEG;
static const long Cryptography_HAS_ALPN;
static const long Cryptography_HAS_SET_CERT_CB;

static const long SSL_FILETYPE_PEM;
static const long SSL_FILETYPE_ASN1;
static const long SSL_ERROR_NONE;
static const long SSL_ERROR_ZERO_RETURN;
static const long SSL_ERROR_WANT_READ;
static const long SSL_ERROR_WANT_WRITE;
static const long SSL_ERROR_WANT_X509_LOOKUP;
static const long SSL_ERROR_SYSCALL;
static const long SSL_ERROR_SSL;
static const long SSL_SENT_SHUTDOWN;
static const long SSL_RECEIVED_SHUTDOWN;
static const long SSL_OP_NO_SSLv2;
static const long SSL_OP_NO_SSLv3;
static const long SSL_OP_NO_TLSv1;
static const long SSL_OP_NO_TLSv1_1;
static const long SSL_OP_NO_TLSv1_2;
static const long SSL_OP_NO_COMPRESSION;
static const long SSL_OP_SINGLE_DH_USE;
static const long SSL_OP_EPHEMERAL_RSA;
static const long SSL_OP_MICROSOFT_SESS_ID_BUG;
static const long SSL_OP_NETSCAPE_CHALLENGE_BUG;
static const long SSL_OP_NETSCAPE_REUSE_CIPHER_CHANGE_BUG;
static const long SSL_OP_SSLREF2_REUSE_CERT_TYPE_BUG;
static const long SSL_OP_MICROSOFT_BIG_SSLV3_BUFFER;
static const long SSL_OP_MSIE_SSLV2_RSA_PADDING;
static const long SSL_OP_SSLEAY_080_CLIENT_DH_BUG;
static const long SSL_OP_TLS_D5_BUG;
static const long SSL_OP_TLS_BLOCK_PADDING_BUG;
static const long SSL_OP_DONT_INSERT_EMPTY_FRAGMENTS;
static const long SSL_OP_CIPHER_SERVER_PREFERENCE;
static const long SSL_OP_TLS_ROLLBACK_BUG;
static const long SSL_OP_PKCS1_CHECK_1;
static const long SSL_OP_PKCS1_CHECK_2;
static const long SSL_OP_NETSCAPE_CA_DN_BUG;
static const long SSL_OP_NETSCAPE_DEMO_CIPHER_CHANGE_BUG;
static const long SSL_OP_NO_QUERY_MTU;
static const long SSL_OP_COOKIE_EXCHANGE;
static const long SSL_OP_NO_TICKET;
static const long SSL_OP_ALL;
static const long SSL_OP_SINGLE_ECDH_USE;
static const long SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION;
static const long SSL_OP_LEGACY_SERVER_CONNECT;
static const long SSL_VERIFY_PEER;
static const long SSL_VERIFY_FAIL_IF_NO_PEER_CERT;
static const long SSL_VERIFY_CLIENT_ONCE;
static const long SSL_VERIFY_NONE;
static const long SSL_SESS_CACHE_OFF;
static const long SSL_SESS_CACHE_CLIENT;
static const long SSL_SESS_CACHE_SERVER;
static const long SSL_SESS_CACHE_BOTH;
static const long SSL_SESS_CACHE_NO_AUTO_CLEAR;
static const long SSL_SESS_CACHE_NO_INTERNAL_LOOKUP;
static const long SSL_SESS_CACHE_NO_INTERNAL_STORE;
static const long SSL_SESS_CACHE_NO_INTERNAL;
static const long SSL_ST_CONNECT;
static const long SSL_ST_ACCEPT;
static const long SSL_ST_MASK;
static const long SSL_ST_INIT;
static const long SSL_ST_BEFORE;
static const long SSL_ST_OK;
static const long SSL_ST_RENEGOTIATE;
static const long SSL_CB_LOOP;
static const long SSL_CB_EXIT;
static const long SSL_CB_READ;
static const long SSL_CB_WRITE;
static const long SSL_CB_ALERT;
static const long SSL_CB_READ_ALERT;
static const long SSL_CB_WRITE_ALERT;
static const long SSL_CB_ACCEPT_LOOP;
static const long SSL_CB_ACCEPT_EXIT;
static const long SSL_CB_CONNECT_LOOP;
static const long SSL_CB_CONNECT_EXIT;
static const long SSL_CB_HANDSHAKE_START;
static const long SSL_CB_HANDSHAKE_DONE;
static const long SSL_MODE_RELEASE_BUFFERS;
static const long SSL_MODE_ENABLE_PARTIAL_WRITE;
static const long SSL_MODE_ACCEPT_MOVING_WRITE_BUFFER;
static const long SSL_MODE_AUTO_RETRY;
static const long SSL3_RANDOM_SIZE;

typedef ... SSL_METHOD;
typedef ... SSL_CTX;

typedef struct {
    int master_key_length;
    unsigned char master_key[...];
    unsigned int session_id_length;
    unsigned char session_id[...];
    unsigned int sid_ctx_length;
    unsigned char sid_ctx[...];
    ...;
} SSL_SESSION;

typedef struct {
    unsigned char server_random[...];
    unsigned char client_random[...];
    ...;
} SSL3_STATE;

typedef struct {
    int version;
    int type;
    SSL3_STATE *s3;
    SSL_SESSION *session;
    ...;
} SSL;

static const long TLSEXT_NAMETYPE_host_name;

typedef ... SSL_CIPHER;
typedef ... Cryptography_STACK_OF_SSL_CIPHER;
typedef ... COMP_METHOD;
"""

FUNCTIONS = """
void SSL_load_error_strings(void);
int SSL_library_init(void);

/*  SSL */
const char *SSL_state_string_long(const SSL *);
SSL_SESSION *SSL_get1_session(SSL *);
int SSL_set_session(SSL *, SSL_SESSION *);
int SSL_get_verify_mode(const SSL *);
void SSL_set_verify(SSL *, int, int (*)(int, X509_STORE_CTX *));
void SSL_set_verify_depth(SSL *, int);
int SSL_get_verify_depth(const SSL *);
int (*SSL_get_verify_callback(const SSL *))(int, X509_STORE_CTX *);
void SSL_set_info_callback(SSL *ssl, void (*)(const SSL *, int, int));
void (*SSL_get_info_callback(const SSL *))(const SSL *, int, int);
SSL *SSL_new(SSL_CTX *);
void SSL_free(SSL *);
int SSL_set_fd(SSL *, int);
void SSL_set_bio(SSL *, BIO *, BIO *);
void SSL_set_connect_state(SSL *);
void SSL_set_accept_state(SSL *);
void SSL_set_shutdown(SSL *, int);
int SSL_get_shutdown(const SSL *);
int SSL_pending(const SSL *);
int SSL_write(SSL *, const void *, int);
int SSL_read(SSL *, void *, int);
int SSL_peek(SSL *, void *, int);
X509 *SSL_get_peer_certificate(const SSL *);
int SSL_get_ex_data_X509_STORE_CTX_idx(void);

int SSL_use_certificate(SSL *, X509 *);
int SSL_use_certificate_ASN1(SSL *, const unsigned char *, int);
int SSL_use_certificate_file(SSL *, const char *, int);
int SSL_use_PrivateKey(SSL *, EVP_PKEY *);
int SSL_use_PrivateKey_ASN1(int, SSL *, const unsigned char *, long);
int SSL_use_PrivateKey_file(SSL *, const char *, int);
int SSL_check_private_key(const SSL *);

Cryptography_STACK_OF_X509 *SSL_get_peer_cert_chain(const SSL *);
Cryptography_STACK_OF_X509_NAME *SSL_get_client_CA_list(const SSL *);

int SSL_get_error(const SSL *, int);
int SSL_do_handshake(SSL *);
int SSL_shutdown(SSL *);
int SSL_renegotiate(SSL *);
int SSL_renegotiate_pending(SSL *);
const char *SSL_get_cipher_list(const SSL *, int);
Cryptography_STACK_OF_SSL_CIPHER *SSL_get_ciphers(const SSL *);

/*  context */
void SSL_CTX_free(SSL_CTX *);
long SSL_CTX_set_timeout(SSL_CTX *, long);
int SSL_CTX_set_default_verify_paths(SSL_CTX *);
void SSL_CTX_set_verify(SSL_CTX *, int, int (*)(int, X509_STORE_CTX *));
void SSL_CTX_set_verify_depth(SSL_CTX *, int);
int (*SSL_CTX_get_verify_callback(const SSL_CTX *))(int, X509_STORE_CTX *);
int SSL_CTX_get_verify_mode(const SSL_CTX *);
int SSL_CTX_get_verify_depth(const SSL_CTX *);
int SSL_CTX_set_cipher_list(SSL_CTX *, const char *);
int SSL_CTX_load_verify_locations(SSL_CTX *, const char *, const char *);
void SSL_CTX_set_default_passwd_cb(SSL_CTX *, pem_password_cb *);
void SSL_CTX_set_default_passwd_cb_userdata(SSL_CTX *, void *);
int SSL_CTX_use_certificate(SSL_CTX *, X509 *);
int SSL_CTX_use_certificate_ASN1(SSL_CTX *, int, const unsigned char *);
int SSL_CTX_use_certificate_file(SSL_CTX *, const char *, int);
int SSL_CTX_use_certificate_chain_file(SSL_CTX *, const char *);
int SSL_CTX_use_PrivateKey(SSL_CTX *, EVP_PKEY *);
int SSL_CTX_use_PrivateKey_ASN1(int, SSL_CTX *, const unsigned char *, long);
int SSL_CTX_use_PrivateKey_file(SSL_CTX *, const char *, int);
int SSL_CTX_check_private_key(const SSL_CTX *);
void SSL_CTX_set_cert_verify_callback(SSL_CTX *,
                                      int (*)(X509_STORE_CTX *,void *),
                                      void *);

void SSL_CTX_set_cert_store(SSL_CTX *, X509_STORE *);
X509_STORE *SSL_CTX_get_cert_store(const SSL_CTX *);
int SSL_CTX_add_client_CA(SSL_CTX *, X509 *);

void SSL_CTX_set_client_CA_list(SSL_CTX *, Cryptography_STACK_OF_X509_NAME *);

/*  SSL_SESSION */
void SSL_SESSION_free(SSL_SESSION *);

/* Information about actually used cipher */
const char *SSL_CIPHER_get_name(const SSL_CIPHER *);
int SSL_CIPHER_get_bits(const SSL_CIPHER *, int *);
char *SSL_CIPHER_get_version(const SSL_CIPHER *);

size_t SSL_get_finished(const SSL *, void *, size_t);
size_t SSL_get_peer_finished(const SSL *, void *, size_t);
"""

MACROS = """
/* not a macro, but older OpenSSLs don't pass the args as const */
char *SSL_CIPHER_description(const SSL_CIPHER *, char *, int);
int SSL_SESSION_print(BIO *, const SSL_SESSION *);

/* not macros, but will be conditionally bound so can't live in functions */
const COMP_METHOD *SSL_get_current_compression(SSL *);
const COMP_METHOD *SSL_get_current_expansion(SSL *);
const char *SSL_COMP_get_name(const COMP_METHOD *);
int SSL_CTX_set_client_cert_engine(SSL_CTX *, ENGINE *);

unsigned long SSL_set_mode(SSL *, unsigned long);
unsigned long SSL_get_mode(SSL *);

unsigned long SSL_set_options(SSL *, unsigned long);
unsigned long SSL_get_options(SSL *);

int SSL_want_read(const SSL *);
int SSL_want_write(const SSL *);

long SSL_total_renegotiations(SSL *);
long SSL_get_secure_renegotiation_support(SSL *);

/* Defined as unsigned long because SSL_OP_ALL is greater than signed 32-bit
   and Windows defines long as 32-bit. */
unsigned long SSL_CTX_set_options(SSL_CTX *, unsigned long);
unsigned long SSL_CTX_get_options(SSL_CTX *);
unsigned long SSL_CTX_set_mode(SSL_CTX *, unsigned long);
unsigned long SSL_CTX_get_mode(SSL_CTX *);
unsigned long SSL_CTX_set_session_cache_mode(SSL_CTX *, unsigned long);
unsigned long SSL_CTX_get_session_cache_mode(SSL_CTX *);
unsigned long SSL_CTX_set_tmp_dh(SSL_CTX *, DH *);
unsigned long SSL_CTX_set_tmp_ecdh(SSL_CTX *, EC_KEY *);
unsigned long SSL_CTX_add_extra_chain_cert(SSL_CTX *, X509 *);

/*- These aren't macros these functions are all const X on openssl > 1.0.x -*/

/*  methods */

/* SSLv2 support is compiled out of some versions of OpenSSL.  These will
 * get special support when we generate the bindings so that if they are
 * available they will be wrapped, but if they are not they won't cause
 * problems (like link errors).
 */
const SSL_METHOD *SSLv2_method(void);
const SSL_METHOD *SSLv2_server_method(void);
const SSL_METHOD *SSLv2_client_method(void);

/*
 * TLSv1_1 and TLSv1_2 are recent additions.  Only sufficiently new versions of
 * OpenSSL support them.
 */
const SSL_METHOD *TLSv1_1_method(void);
const SSL_METHOD *TLSv1_1_server_method(void);
const SSL_METHOD *TLSv1_1_client_method(void);

const SSL_METHOD *TLSv1_2_method(void);
const SSL_METHOD *TLSv1_2_server_method(void);
const SSL_METHOD *TLSv1_2_client_method(void);

const SSL_METHOD *SSLv3_method(void);
const SSL_METHOD *SSLv3_server_method(void);
const SSL_METHOD *SSLv3_client_method(void);

const SSL_METHOD *TLSv1_method(void);
const SSL_METHOD *TLSv1_server_method(void);
const SSL_METHOD *TLSv1_client_method(void);

const SSL_METHOD *DTLSv1_method(void);
const SSL_METHOD *DTLSv1_server_method(void);
const SSL_METHOD *DTLSv1_client_method(void);

const SSL_METHOD *SSLv23_method(void);
const SSL_METHOD *SSLv23_server_method(void);
const SSL_METHOD *SSLv23_client_method(void);

/*- These aren't macros these arguments are all const X on openssl > 1.0.x -*/
SSL_CTX *SSL_CTX_new(SSL_METHOD *);
long SSL_CTX_get_timeout(const SSL_CTX *);

const SSL_CIPHER *SSL_get_current_cipher(const SSL *);
const char *SSL_get_version(const SSL *);
int SSL_version(const SSL *);

/* SNI APIs were introduced in OpenSSL 1.0.0.  To continue to support
 * earlier versions some special handling of these is necessary.
 */
const char *SSL_get_servername(const SSL *, const int);
void SSL_set_tlsext_host_name(SSL *, char *);
void SSL_CTX_set_tlsext_servername_callback(
    SSL_CTX *,
    int (*)(const SSL *, int *, void *));

/* These were added in OpenSSL 0.9.8h, but since version testing in OpenSSL
   is fraught with peril thanks to OS distributions we check some constants
   to determine if they are supported or not */
long SSL_set_tlsext_status_ocsp_resp(SSL *, unsigned char *, int);
long SSL_get_tlsext_status_ocsp_resp(SSL *, const unsigned char **);
long SSL_set_tlsext_status_type(SSL *, long);
long SSL_CTX_set_tlsext_status_cb(SSL_CTX *, int(*)(SSL *, void *));
long SSL_CTX_set_tlsext_status_arg(SSL_CTX *, void *);

long SSL_session_reused(SSL *);

/* The following were macros in 0.9.8e. Once we drop support for RHEL/CentOS 5
   we should move these back to FUNCTIONS. */
void SSL_CTX_set_info_callback(SSL_CTX *, void (*)(const SSL *, int, int));
void (*SSL_CTX_get_info_callback(SSL_CTX *))(const SSL *, int, int);
/* This function does not exist in 0.9.8e. Once we drop support for
   RHEL/CentOS 5 this can be moved back to FUNCTIONS. */
SSL_CTX *SSL_set_SSL_CTX(SSL *, SSL_CTX *);

const SSL_METHOD *Cryptography_SSL_CTX_get_method(const SSL_CTX *);

/* NPN APIs were introduced in OpenSSL 1.0.1.  To continue to support earlier
 * versions some special handling of these is necessary.
 */
void SSL_CTX_set_next_protos_advertised_cb(SSL_CTX *,
                                           int (*)(SSL *,
                                                   const unsigned char **,
                                                   unsigned int *,
                                                   void *),
                                           void *);
void SSL_CTX_set_next_proto_select_cb(SSL_CTX *,
                                      int (*)(SSL *,
                                              unsigned char **,
                                              unsigned char *,
                                              const unsigned char *,
                                              unsigned int,
                                              void *),
                                      void *);
int SSL_select_next_proto(unsigned char **, unsigned char *,
                          const unsigned char *, unsigned int,
                          const unsigned char *, unsigned int);
void SSL_get0_next_proto_negotiated(const SSL *,
                                    const unsigned char **, unsigned *);

int sk_SSL_CIPHER_num(Cryptography_STACK_OF_SSL_CIPHER *);
SSL_CIPHER *sk_SSL_CIPHER_value(Cryptography_STACK_OF_SSL_CIPHER *, int);

/* ALPN APIs were introduced in OpenSSL 1.0.2.  To continue to support earlier
 * versions some special handling of these is necessary.
 */
int SSL_CTX_set_alpn_protos(SSL_CTX *, const unsigned char *, unsigned);
int SSL_set_alpn_protos(SSL *, const unsigned char *, unsigned);
void SSL_CTX_set_alpn_select_cb(SSL_CTX *,
                                int (*) (SSL *,
                                         const unsigned char **,
                                         unsigned char *,
                                         const unsigned char *,
                                         unsigned int,
                                         void *),
                                void *);
void SSL_get0_alpn_selected(const SSL *, const unsigned char **, unsigned *);

long SSL_get_server_tmp_key(SSL *, EVP_PKEY **);

/* SSL_CTX_set_cert_cb is introduced in OpenSSL 1.0.2. To continue to support
 * earlier versions some special handling of these is necessary.
 */
void SSL_CTX_set_cert_cb(SSL_CTX *, int (*)(SSL *, void *), void *);
void SSL_set_cert_cb(SSL *, int (*)(SSL *, void *), void *);
"""

CUSTOMIZATIONS = """
/** Secure renegotiation is supported in OpenSSL >= 0.9.8m
 *  But some Linux distributions have back ported some features.
 */
#ifndef SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION
static const long Cryptography_HAS_SECURE_RENEGOTIATION = 0;
long (*SSL_get_secure_renegotiation_support)(SSL *) = NULL;
const long SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION = 0;
const long SSL_OP_LEGACY_SERVER_CONNECT = 0;
#else
static const long Cryptography_HAS_SECURE_RENEGOTIATION = 1;
#endif
#ifdef OPENSSL_NO_SSL2
static const long Cryptography_HAS_SSL2 = 0;
SSL_METHOD* (*SSLv2_method)(void) = NULL;
SSL_METHOD* (*SSLv2_client_method)(void) = NULL;
SSL_METHOD* (*SSLv2_server_method)(void) = NULL;
#else
static const long Cryptography_HAS_SSL2 = 1;
#endif

#ifdef OPENSSL_NO_SSL3_METHOD
static const long Cryptography_HAS_SSL3_METHOD = 0;
SSL_METHOD* (*SSLv3_method)(void) = NULL;
SSL_METHOD* (*SSLv3_client_method)(void) = NULL;
SSL_METHOD* (*SSLv3_server_method)(void) = NULL;
#else
static const long Cryptography_HAS_SSL3_METHOD = 1;
#endif

#ifdef SSL_CTRL_SET_TLSEXT_HOSTNAME
static const long Cryptography_HAS_TLSEXT_HOSTNAME = 1;
#else
static const long Cryptography_HAS_TLSEXT_HOSTNAME = 0;
void (*SSL_set_tlsext_host_name)(SSL *, char *) = NULL;
const char* (*SSL_get_servername)(const SSL *, const int) = NULL;
void (*SSL_CTX_set_tlsext_servername_callback)(
    SSL_CTX *,
    int (*)(const SSL *, int *, void *)) = NULL;
#endif

#ifdef SSL_CTRL_SET_TLSEXT_STATUS_REQ_CB
static const long Cryptography_HAS_TLSEXT_STATUS_REQ_CB = 1;
#else
static const long Cryptography_HAS_TLSEXT_STATUS_REQ_CB = 0;
long (*SSL_CTX_set_tlsext_status_cb)(SSL_CTX *, int(*)(SSL *, void *)) = NULL;
long (*SSL_CTX_set_tlsext_status_arg)(SSL_CTX *, void *) = NULL;
#endif

#ifdef SSL_CTRL_SET_TLSEXT_STATUS_REQ_OCSP_RESP
static const long Cryptography_HAS_STATUS_REQ_OCSP_RESP = 1;
#else
static const long Cryptography_HAS_STATUS_REQ_OCSP_RESP = 0;
long (*SSL_set_tlsext_status_ocsp_resp)(SSL *, unsigned char *, int) = NULL;
long (*SSL_get_tlsext_status_ocsp_resp)(SSL *, const unsigned char **) = NULL;
#endif

#ifdef SSL_CTRL_SET_TLSEXT_STATUS_REQ_TYPE
static const long Cryptography_HAS_TLSEXT_STATUS_REQ_TYPE = 1;
#else
static const long Cryptography_HAS_TLSEXT_STATUS_REQ_TYPE = 0;
long (*SSL_set_tlsext_status_type)(SSL *, long) = NULL;
#endif

#ifdef SSL_MODE_RELEASE_BUFFERS
static const long Cryptography_HAS_RELEASE_BUFFERS = 1;
#else
static const long Cryptography_HAS_RELEASE_BUFFERS = 0;
const long SSL_MODE_RELEASE_BUFFERS = 0;
#endif

#ifdef SSL_OP_NO_COMPRESSION
static const long Cryptography_HAS_OP_NO_COMPRESSION = 1;
#else
static const long Cryptography_HAS_OP_NO_COMPRESSION = 0;
const long SSL_OP_NO_COMPRESSION = 0;
#endif

#ifdef SSL_OP_NO_TLSv1_1
static const long Cryptography_HAS_TLSv1_1 = 1;
#else
static const long Cryptography_HAS_TLSv1_1 = 0;
static const long SSL_OP_NO_TLSv1_1 = 0;
SSL_METHOD* (*TLSv1_1_method)(void) = NULL;
SSL_METHOD* (*TLSv1_1_client_method)(void) = NULL;
SSL_METHOD* (*TLSv1_1_server_method)(void) = NULL;
#endif

#ifdef SSL_OP_NO_TLSv1_2
static const long Cryptography_HAS_TLSv1_2 = 1;
#else
static const long Cryptography_HAS_TLSv1_2 = 0;
static const long SSL_OP_NO_TLSv1_2 = 0;
SSL_METHOD* (*TLSv1_2_method)(void) = NULL;
SSL_METHOD* (*TLSv1_2_client_method)(void) = NULL;
SSL_METHOD* (*TLSv1_2_server_method)(void) = NULL;
#endif

#ifdef SSL_OP_MSIE_SSLV2_RSA_PADDING
static const long Cryptography_HAS_SSL_OP_MSIE_SSLV2_RSA_PADDING = 1;
#else
static const long Cryptography_HAS_SSL_OP_MSIE_SSLV2_RSA_PADDING = 0;
const long SSL_OP_MSIE_SSLV2_RSA_PADDING = 0;
#endif

#ifdef OPENSSL_NO_EC
long (*SSL_CTX_set_tmp_ecdh)(SSL_CTX *, EC_KEY *) = NULL;
#endif

#ifdef SSL_OP_NO_TICKET
static const long Cryptography_HAS_SSL_OP_NO_TICKET = 1;
#else
static const long Cryptography_HAS_SSL_OP_NO_TICKET = 0;
const long SSL_OP_NO_TICKET = 0;
#endif

/* OpenSSL 0.9.8f+ */
#if OPENSSL_VERSION_NUMBER >= 0x00908070L
static const long Cryptography_HAS_SSL_SET_SSL_CTX = 1;
#else
static const long Cryptography_HAS_SSL_SET_SSL_CTX = 0;
static const long TLSEXT_NAMETYPE_host_name = 0;
SSL_CTX *(*SSL_set_SSL_CTX)(SSL *, SSL_CTX *) = NULL;
#endif

/* NetBSD shipped without including d1_meth.c. This workaround checks to see
   if the version of NetBSD we're currently running on is old enough to
   have the bug and provides an empty implementation so we can link and
   then remove the function from the ffi object. */
#ifdef __NetBSD__
#  include <sys/param.h>
#  if (__NetBSD_Version__ < 699003800)
static const long Cryptography_HAS_NETBSD_D1_METH = 0;
const SSL_METHOD *DTLSv1_method(void) {
    return NULL;
}
#  else
static const long Cryptography_HAS_NETBSD_D1_METH = 1;
#  endif
#else
static const long Cryptography_HAS_NETBSD_D1_METH = 1;
#endif

/* Workaround for #794 caused by cffi const** bug. */
const SSL_METHOD *Cryptography_SSL_CTX_get_method(const SSL_CTX *ctx) {
    return ctx->method;
}

/* Because OPENSSL defines macros that claim lack of support for things, rather
 * than macros that claim support for things, we need to do a version check in
 * addition to a definition check. NPN was added in 1.0.1: for any version
 * before that, there is no compatibility.
 */
#if defined(OPENSSL_NO_NEXTPROTONEG) || OPENSSL_VERSION_NUMBER < 0x1000100fL
static const long Cryptography_HAS_NEXTPROTONEG = 0;
void (*SSL_CTX_set_next_protos_advertised_cb)(SSL_CTX *,
                                              int (*)(SSL *,
                                                      const unsigned char **,
                                                      unsigned int *,
                                                      void *),
                                              void *) = NULL;
void (*SSL_CTX_set_next_proto_select_cb)(SSL_CTX *,
                                         int (*)(SSL *,
                                                 unsigned char **,
                                                 unsigned char *,
                                                 const unsigned char *,
                                                 unsigned int,
                                                 void *),
                                         void *) = NULL;
int (*SSL_select_next_proto)(unsigned char **, unsigned char *,
                             const unsigned char *, unsigned int,
                             const unsigned char *, unsigned int) = NULL;
void (*SSL_get0_next_proto_negotiated)(const SSL *,
                                       const unsigned char **,
                                       unsigned *) = NULL;
#else
static const long Cryptography_HAS_NEXTPROTONEG = 1;
#endif

/* ALPN was added in OpenSSL 1.0.2. */
#if OPENSSL_VERSION_NUMBER < 0x10002001L && !defined(LIBRESSL_VERSION_NUMBER)
int (*SSL_CTX_set_alpn_protos)(SSL_CTX *,
                               const unsigned char *,
                               unsigned) = NULL;
int (*SSL_set_alpn_protos)(SSL *, const unsigned char *, unsigned) = NULL;
void (*SSL_CTX_set_alpn_select_cb)(SSL_CTX *,
                                   int (*) (SSL *,
                                            const unsigned char **,
                                            unsigned char *,
                                            const unsigned char *,
                                            unsigned int,
                                            void *),
                                   void *) = NULL;
void (*SSL_get0_alpn_selected)(const SSL *,
                               const unsigned char **,
                               unsigned *) = NULL;
static const long Cryptography_HAS_ALPN = 0;
#else
static const long Cryptography_HAS_ALPN = 1;
#endif

/* SSL_CTX_set_cert_cb was added in OpenSSL 1.0.2. */
#if OPENSSL_VERSION_NUMBER < 0x10002001L || defined(LIBRESSL_VERSION_NUMBER)
void (*SSL_CTX_set_cert_cb)(SSL_CTX *, int (*)(SSL *, void *), void *) = NULL;
void (*SSL_set_cert_cb)(SSL *, int (*)(SSL *, void *), void *) = NULL;
static const long Cryptography_HAS_SET_CERT_CB = 0;
#else
static const long Cryptography_HAS_SET_CERT_CB = 1;
#endif


#if defined(OPENSSL_NO_COMP) || defined(LIBRESSL_VERSION_NUMBER)
static const long Cryptography_HAS_COMPRESSION = 0;
typedef void COMP_METHOD;
#else
static const long Cryptography_HAS_COMPRESSION = 1;
#endif

#if defined(SSL_CTRL_GET_SERVER_TMP_KEY)
static const long Cryptography_HAS_GET_SERVER_TMP_KEY = 1;
#else
static const long Cryptography_HAS_GET_SERVER_TMP_KEY = 0;
long (*SSL_get_server_tmp_key)(SSL *, EVP_PKEY **) = NULL;
#endif

/* Added in 0.9.8i */
#if OPENSSL_VERSION_NUMBER < 0x0090809fL
int (*SSL_CTX_set_client_cert_engine)(SSL_CTX *, ENGINE *) = NULL;
static const long Cryptography_HAS_SSL_CTX_SET_CLIENT_CERT_ENGINE = 0;
# else
static const long Cryptography_HAS_SSL_CTX_SET_CLIENT_CERT_ENGINE = 1;
#endif

"""
