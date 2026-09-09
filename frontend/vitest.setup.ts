import { loadDevMessages, loadErrorMessages } from "@apollo/client/dev";

// By default, Apollo's error messages are minified. For tests, we want to load
// the full messages to make debugging easier.
loadDevMessages();
loadErrorMessages();
