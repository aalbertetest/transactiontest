package pebbletoy

import (
	"bufio"
	"io"
)

func newBufWriter(w io.Writer, size int) *bufio.Writer {
	return bufio.NewWriterSize(w, size)
}
