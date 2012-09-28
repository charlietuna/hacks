#!/usr/bin/python
import sys,sha,hmac; print hmac.new("46DCEAD317FE45D80923EB97E4956410D4CDB2C2".decode("hex"), sys.argv[1].decode("hex"), sha).hexdigest()
