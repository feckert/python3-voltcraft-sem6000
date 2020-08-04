#!/bin/bash


usage() {
	echo "$0 <bluetooth address> <pin>" 1>&2
}

main() {
	ADDRESS="$1"
	PIN="$2"

	SCRIPTDIR="$( dirname "$0" )"

	ORIGINAL_SETTINGS_FILE="original_settings.json"
	SETTINGS_FILE_FOR_TEST="settings_for_integration_test.json"

	TMPFILE="$( mktemp )"

	TEST_FAILED=0

	if [ -f "$SCRIPTDIR/${ORIGINAL_SETTINGS_FILE}" ]
	then
		echo "$SCRIPTDIR/${ORIGINAL_SETTINGS_FILE} already exists ... aborting" 1>&2
		return 1
	fi

	echo "Backing up original settings to $SCRIPTDIR/${ORIGINAL_SETTINGS_FILE} ..." 1>&2
	if ! "$SCRIPTDIR/sem6000-settings-backup-demo.py" "$ADDRESS" "$PIN" > "$SCRIPTDIR/${ORIGINAL_SETTINGS_FILE}"
	then
		echo "Failed to backup current settings ... aborting" 1>&2
		return 1
	fi
	echo "" 1>&2

	echo "Running integration test... " 1>&2
	"$SCRIPTDIR/sem6000-settings-restore-demo.py" "$ADDRESS" "$PIN" "$SCRIPTDIR/${SETTINGS_FILE_FOR_TEST}"
	"$SCRIPTDIR/sem6000-settings-backup-demo.py" "$ADDRESS" "$PIN" > "$TMPFILE"
	if ! diff "$TMPFILE" "${SETTINGS_FILE_FOR_TEST}"
	then
		TEST_FAILED=1
		echo "FAILED" 1>&2 
	fi
	echo "" 1>&2

	echo "Test reading values that are not covered by backup/restore settings script..." 1>&2
	if ! "$SCRIPTDIR/sem6000-read-tests.py" "$ADDRESS" "$PIN"
	then
		TEST_FAILED=1
		echo "FAILED" 1>&2
	fi
	echo "" 1>&2

	echo "Restoring original settings from $SCRIPTDIR/${ORIGINAL_SETTINGS_FILE} ..." 1>&2
	"$SCRIPTDIR/sem6000-settings-restore-demo.py" "$ADDRESS" "$PIN" "$SCRIPTDIR/${ORIGINAL_SETTINGS_FILE}"
	echo "" 1>&2

	if [ "${TEST_FAILED}" == "0" ]
	then
		echo "Test succeeded."
		return 0
	else
		echo "Test failed."
		return 1
	fi
}

if [ $# -lt 2 ]
then
	usage
	exit 1
fi

main "$@"
