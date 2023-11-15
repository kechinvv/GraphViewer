package cfg

import (
	"bytes"
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"golang.org/x/tools/go/cfg"
	"regexp"
	"strings"
)

func getFunctions(code string) []ast.Node {
	var funcs []ast.Node
	fs := token.NewFileSet()

	f, err := parser.ParseFile(fs, "", code, parser.AllErrors)
	if err != nil {
		panic(err)
	}

	ast.Inspect(f, func(node ast.Node) bool {
		if node != nil {
			switch node.(type) {
			case *ast.FuncDecl:
				funcs = append(funcs, node.(*ast.FuncDecl).Body)
			}

		}
		return true
	})

	return funcs
}

func drawNodes(block cfg.Block, sb *strings.Builder, buf bytes.Buffer, s []string) bool {
	if len(block.Succs) == 2 && !strings.Contains(block.String(), "range.") {
		sb.WriteString(fmt.Sprintf("n%dx%d[ shape=diamond, style=filled, label=%q ]\n",
			block.Index, block.Index, s[len(s)-2]))

		if strings.Join(s[:len(s)-2], "\n") != "" {
			sb.WriteString(fmt.Sprintf("n%d -> n%dx%d\n", block.Index, block.Index, block.Index))

			sb.WriteString(fmt.Sprintf("n%d[ shape=box, style=filled, label=%q ]\n",
				block.Index, strings.Join(s[:len(s)-2], "\n")))
		}
	} else if strings.Contains(block.String(), "switch.next") && buf.String() != "" {
		sb.WriteString(fmt.Sprintf("n%d[ shape=diamond, style=filled, label=%q ]\n", block.Index, buf.String()))
	} else if strings.Contains(block.String(), "unreachable.") {
		return false
	} else if buf.String() == "" {
		r := regexp.MustCompile("\\(.*\\)")

		sb.WriteString(fmt.Sprintf(
			"n%d[ fillcolor=lightslategray shape=box, style=filled, label=%q ]\n",
			block.Index, r.FindString(block.String())))
	} else {
		sb.WriteString(fmt.Sprintf("n%d[ shape=box, style=filled, label=%q ]\n", block.Index, buf.String()))
	}

	return true
}

func drawConnections(block cfg.Block, sb *strings.Builder, buf bytes.Buffer, s []string) {
	if len(block.Succs) == 2 && !strings.Contains(block.String(), "range.") {
		for i, succ := range block.Succs {

			if strings.Join(s[:len(s)-2], "\n") != "\n" {
				if len(succ.Succs) == 2 && len(succ.Nodes) == 1 {
					sb.WriteString(fmt.Sprintf("n%dx%d -> n%dx%d[ label=%t  ]\n",
						block.Index, block.Index, succ.Index, succ.Index, i == 0))
				} else {
					sb.WriteString(fmt.Sprintf("n%dx%d -> n%d[ label=%t  ]\n",
						block.Index, block.Index, succ.Index, i == 0))
				}
			}
		}
	} else {
		for _, succ := range block.Succs {
			if len(succ.Succs) == 2 && len(succ.Nodes) == 1 {
				sb.WriteString(fmt.Sprintf("n%d -> n%dx%d\n", block.Index, succ.Index, succ.Index))
			} else {
				sb.WriteString(fmt.Sprintf("n%d -> n%d\n", block.Index, succ.Index))
			}
		}
	}

	if strings.Contains(buf.String(), "return") {
		sb.WriteString(fmt.Sprintf("n%d -> END\n", block.Index))
	}
}

func Create(code string) string {
	funcs := getFunctions(code)
	sb := strings.Builder{}
	fs := token.NewFileSet()

	sb.WriteString("digraph{\n")

	for i, node := range funcs {
		if i > 0 {
			break
		}
		buf := bytes.Buffer{}

		c := cfg.New(node.(*ast.BlockStmt), func(expr *ast.CallExpr) bool {
			return true
		})
		sb.WriteString(fmt.Sprintf("subgraph cluster_%d {\n", i))
		sb.WriteString("ROOT[shape=Mdiamond, label=\"BEGIN\"]\n")
		sb.WriteString("END[shape=Mdiamond, label=\"END\"]\n")
		sb.WriteString("ROOT -> n0\n")

		for _, block := range c.Blocks {
			for _, node := range block.Nodes {
				err := format.Node(&buf, fs, node)
				if err != nil {
					panic(err)
				}
				buf.WriteString("\n")
			}

			s := strings.Split(buf.String(), "\n")
			if !drawNodes(*block, &sb, buf, s) {
				continue
			}
			drawConnections(*block, &sb, buf, s)

			buf.Reset()
		}
		sb.WriteString("}")
	}
	sb.WriteString("}")
	return sb.String()
}
