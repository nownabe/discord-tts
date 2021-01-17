package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/bwmarrin/discordgo"
)

func main() {
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_BOT_TOKEN"))
	if err != nil {
		panic(err)
	}

	dg.AddHandler(handler)
	dg.Identify.Intents = discordgo.MakeIntent(discordgo.IntentsGuildMessages)

	if err := dg.Open(); err != nil {
		panic(err)
	}
	defer dg.Close()

	fmt.Println("Bot is now running. Press CTRL-C to exit.")
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-sc
}

func handler(s *discordgo.Session, m *discordgo.MessageCreate) {
	fmt.Println("⭐⭐⭐⭐⭐")
	fmt.Printf("%+v", s)
	fmt.Println("\n---")
	fmt.Printf("%+v", m)
	fmt.Println("\n---")
	fmt.Printf("%+v", m.Message)

	state := discordgo.NewState()
	vs, err := state.VoiceState(m.Message.GuildID, m.Message.Author.ID)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
	fmt.Println("\n--- Voice State")
	fmt.Printf("%+v", vs)

	/*
		channels, err := s.GuildChannels(m.Message.GuildID)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
		}

		for _, ch := range channels {
			fmt.Println("\n--- channel")
			fmt.Printf("%+v", ch)
		}
	*/

	fmt.Printf("\n\n")
}
