/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package com.hpcloud.mon.common.event;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonRootName;
import com.hpcloud.mon.common.model.alarm.AlarmState;
import com.hpcloud.mon.common.model.metric.MetricDefinition;

/**
 * Represents an alarm state transition having occurred.
 */
@JsonRootName(value = "alarm-transitioned")
public class AlarmStateTransitionedEvent {
  public String tenantId;
  public String alarmId;
  public String alarmDefinitionId;
  public List<MetricDefinition> metrics;
  public String alarmName;
  public String alarmDescription;
  public AlarmState oldState;
  public AlarmState newState;
  public boolean actionsEnabled;
  public String stateChangeReason;
  /** POSIX timestamp */
  public long timestamp;

  public AlarmStateTransitionedEvent() {}

  public AlarmStateTransitionedEvent(String tenantId, String alarmId, String alarmDefinitionId,
      List<MetricDefinition> metrics, String alarmName, String alarmDescription,
      AlarmState oldState, AlarmState newState, boolean actionsEnabled, String stateChangeReason,
      long timestamp) {
    this.tenantId = tenantId;
    this.alarmId = alarmId;
    this.alarmDefinitionId = alarmDefinitionId;
    this.metrics = metrics;
    this.alarmName = alarmName;
    this.alarmDescription = alarmDescription;
    this.oldState = oldState;
    this.newState = newState;
    this.actionsEnabled = actionsEnabled;
    this.stateChangeReason = stateChangeReason;
    this.timestamp = timestamp;
  }

  @Override
  public String toString() {
    return "AlarmStateTransitionedEvent [tenantId=" + tenantId + ", alarmId=" + alarmId
        + ", alarmDefinitionId=" + alarmDefinitionId + ", metrics=" + metrics + ", alarmName="
        + alarmName + ", alarmDescription=" + alarmDescription + ", oldState=" + oldState
        + ", newState=" + newState + ", actionsEnabled=" + actionsEnabled + ", stateChangeReason="
        + stateChangeReason + ", timestamp=" + timestamp + "]";
  }
}
