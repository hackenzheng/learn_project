//channel使用

package main

import "fmt"


//后面的反引号是用于转成yaml文件时用到的  https://blog.csdn.net/jason_cuijiahui/article/details/82987091
type Config struct {
    AgentPort           int      `yaml:"agentPort,omitempty"`
    Image               string   `yaml:"image,omitempty"`
    DebugAgentDaemonSet string   `yaml:"debugAgentDaemonset,omitempty"`
    DebugAgentNamespace string   `yaml:"debugAgentNamespace,omitempty"`
    Command             []string `yaml:"command,omitempty"`
    PortForward         bool     `yaml:"portForward,omitempty"`
    Agentless           bool     `yaml:"agentless,omitempty"`
    AgentPodNamePrefix  string   `yaml:"agentPodNamePrefix,omitempty"`
    AgentPodNamespace   string   `yaml:"agentPodNamespace,omitempty"`
    AgentImage          string   `yaml:"agentImage,omitempty"`

    // deprecated
    AgentPortOld int `yaml:"agent_port,omitempty"`
}


func main() {
    a := Config{}  //需要提供初始值，即使为空
    fmt.Println(a)
    fmt.Println(a.AgentPort)

}