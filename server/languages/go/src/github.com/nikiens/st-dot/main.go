package main

import (
	"bufio"
	"fmt"
	"os"
	"st-dot/ast"
	"st-dot/cfg"

	"github.com/thatisuday/commando"
)

type tree int

const (
	Ast tree = iota
	Cfg
)

func transfer(t tree, output string, input string) {
	var file *os.File

	dat, err := os.ReadFile(input)
	if err != nil {
		fmt.Println("Error opening file: " + err.Error())
	}

	if output == "/dev/stdout" {
		f := os.Stdout
		file = f
	} else {
		f, err := os.OpenFile(output, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		file = f
		if err != nil {
			panic(err)
		}
	}

	writer := bufio.NewWriter(file)

	if t == Ast {
		_, err := writer.WriteString(ast.Create(string(dat)))
		if err != nil {
			fmt.Println(dat)
			panic(err)
		}
	} else if t == Cfg {
		_, err := writer.WriteString(cfg.Create(string(dat)))
		if err != nil {
			panic(err)
		}
	}

	writer.Flush()
}

func main() {
	commando.
		SetExecutableName("go-st").
		SetVersion("0.0.1").
		SetDescription(".dot graph generator for Golang's AST and CFG")

	commando.
		Register(nil).
		AddFlag("output, o", "output file", commando.String, "/dev/stdout").
		AddFlag("ast", "print ast dot graph", commando.Bool, nil).
		AddFlag("cfg", "print cfg dot graph", commando.Bool, nil).
		AddArgument("input", "go file to analyze", "").
		SetAction(func(args map[string]commando.ArgValue, flags map[string]commando.FlagValue) {
			input := args["input"].Value
			output, _ := flags["output"].GetString()

			astEnabled, _ := flags["ast"].GetBool()
			cfgEnabled, _ := flags["cfg"].GetBool()

			if (astEnabled && cfgEnabled) || (!astEnabled && !cfgEnabled) {
				fmt.Println("Either ast or cfg must be specified")
				os.Exit(1)
			}

			if astEnabled {
				transfer(Ast, output, input)
			} else if cfgEnabled {
				transfer(Cfg, output, input)
			}
		})

	commando.Parse(nil)
}
