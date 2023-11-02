# SPDX-License-Identifier: AGPL-3.0-or-later

TOPTARGETS := all clean test build

all: test
test:
	@../prj cmd msg.build TEST "scripts/.*sh"
	@shellcheck -x -s bash *.sh

.PHONY: $(TOPTARGETS)
